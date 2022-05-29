import traceback
from copy import deepcopy
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, IntegrityError
from django.db.transaction import atomic

from app.air.models import *
from app.air.services.travelpayouts import TravelpayoutsService
from app.base.logs import warning
from app.geo.models import *
from app.tickets.components.services.session import TicketsSessionService
from app.tickets.models import *


def _parse_gates_info(results):
    gates_info = {}
    for o in results:
        gates_info |= {int(k): v for k, v in o['gates_info'].items()}
    return gates_info


def _parse_flight_info(results):
    flight_info = {}
    for o in results:
        flight_info |= o['flight_info']
    return flight_info


def _parse_xterms(raw_xterms):
    xterms = []
    for gate_id, xterm in raw_xterms.items():
        tariffs = [tariff | {'gate_id': int(gate_id)} for tariff in xterm.values()]
        tariffs.sort(key=lambda _tariff: _tariff['price'])
        xterms.append(tariffs)
    return xterms


def _parse_proposals(results) -> list[dict]:
    proposals = []
    [proposals.extend(result['proposals']) for result in results]
    sign_proposals = {}
    for proposal in proposals:
        if proposal['sign'] in sign_proposals:
            saved_proposal = sign_proposals[proposal['sign']]
            saved_proposal['xterms'].extend(_parse_xterms(proposal['xterms']))
            trips = [trip['flight'] for trip in proposal['segment']]
            saved_trips: list = saved_proposal['trips']
            for trip_index, saved_trip in enumerate(saved_trips):
                trip = trips[trip_index]
                assert len(trip) == len(saved_trip)
                for segment_index, saved_segment in enumerate(saved_trip):
                    segment = trip[segment_index]
                    if not saved_segment.get('aircraft') or len(
                        saved_segment['aircraft']
                    ) < len(segment.get('aircraft', '')):
                        saved_segment['aircraft'] = segment.get('aircraft')
        else:
            sign_proposals[proposal['sign']] = {
                'xterms': _parse_xterms(proposal['xterms']),
                'trips': [trip['flight'] for trip in proposal['segment']]
            }
    for proposal in sign_proposals.values():
        proposal['xterms'] = list(filter(bool, proposal['xterms']))
        proposal['xterms'].sort(key=lambda _xterm: _xterm[0]['price'])
    proposals = [
        proposal | {'sign': sign} for sign, proposal in sign_proposals.items() if
        proposal['xterms']
    ]
    proposals.sort(key=lambda _proposal: _proposal['xterms'][0][0]['price'])
    return proposals


def _parse_flights_tariff(flights_tariff):
    if not flights_tariff:
        return None
    try:
        count, weight = flights_tariff.split('PC')
        return int(count) * int(weight)
    except ValueError:
        return None


def _best_tariff_by_currency(tariffs, currency):
    min_price = None
    for tariff in tariffs:
        if currency.lower() == tariff['currency'].lower():
            tariff_price = tariff['price']
            if min_price is None:
                min_price = tariff_price
            elif min_price > tariff_price:
                min_price = tariff_price
    return min_price


def _create_offers(gates_info, ticket, xterms) -> Offer | None:
    best_offer = None
    for tariffs in xterms:
        best_tariff = tariffs[0]
        gate_id = best_tariff['gate_id']
        offer = Offer.objects.create(
            ticket=ticket, gate_id=gate_id, title=gates_info[gate_id]['label'],
            url=best_tariff['url'], price=best_tariff['price']
        )
        if best_offer:
            if best_offer.price > offer.price:
                best_offer = offer
        else:
            best_offer = offer
    return best_offer


def _update_offers(gates_info, ticket, xterms) -> None:
    best_offer = None
    for tariffs in xterms:
        best_tariff = tariffs[0]
        gate_id = best_tariff['gate_id']
        try:
            offer = Offer.objects.get(ticket=ticket, gate_id=gate_id)
        except Offer.DoesNotExist:
            offer = Offer.objects.create(
                ticket=ticket, gate_id=gate_id, title=gates_info[gate_id]['label'],
                price=best_tariff['price'], url=best_tariff['url']
            )
        if best_offer:
            if best_offer.price > offer.price:
                best_offer = offer
        else:
            best_offer = offer
    ticket.best_offer = best_offer


def _parse_weight_limits(xterms) -> dict[str, list]:
    handbags_weights = None
    baggage_weights = None
    for tariffs in xterms:
        if handbags_weights is None:
            tariff = tariffs[0]
            handbags_weights = [
                [None] * len(flight_handbags)
                for flight_handbags in tariff['flights_handbags']
            ]
            baggage_weights = deepcopy(handbags_weights)
        for tariff in tariffs:
            handbags_tariffs = tariff['flights_handbags']
            baggage_tariffs = tariff['flights_baggage']
            for fhs_i, flight_handbags in enumerate(handbags_weights):
                for fh_i, flight_handbag in enumerate(flight_handbags):
                    if flight_handbag is None:
                        flight_handbags[fh_i] = _parse_flights_tariff(
                            handbags_tariffs[fhs_i][fh_i]
                        )
            for fbs_i, flight_baggage in enumerate(baggage_weights):
                for fb_i, flight_bag in enumerate(flight_baggage):
                    if flight_bag is None:
                        flight_baggage[fb_i] = _parse_flights_tariff(
                            baggage_tariffs[fbs_i][fb_i]
                        )
            for i in range(len(handbags_weights)):
                if None not in handbags_weights[i] + baggage_weights[i]:
                    break
    return {'handbags_weights': handbags_weights, 'baggage_weights': baggage_weights}


def _parse_convenience(amenities, convenience):
    if amenities is None:
        return None
    if convenience == 'alcohol':
        info = amenities.get('beverage')
        if info is None:
            return None
        if info['exists'] and info['type'] == 'alcoholic_and_nonalcoholic':
            return True
        return False
    info = amenities.get(convenience)
    if info is None:
        return None
    if not info['exists']:
        return False
    if convenience == 'beverage':
        return True
    return True


def _create_about(flight_info, raw_segment, segment):
    flight_class = FlightClass(raw_segment['trip_class'])
    airline = Airline.objects.get(code=raw_segment['operating_carrier'])
    amenities = flight_info.get(
        f'{flight_class.name}{airline.code}{raw_segment["number"]}', {}
    ).get('amenities')
    About.objects.create(
        segment=segment, airline=airline, aircraft=raw_segment.get('aircraft', '') or '',
        food=_parse_convenience(amenities, 'food'),
        entertainment=_parse_convenience(amenities, 'entertainment'),
        alcohol=_parse_convenience(amenities, 'alcohol'),
        beverage=_parse_convenience(amenities, 'beverage'),
        power=_parse_convenience(amenities, 'power'),
        wifi=_parse_convenience(amenities, 'wifi')
    )


def _parse_time(date_, time):
    return datetime.fromisoformat(f'{date_}T{time}:00+00:00')


def _create_segment(trip, raw_segment, flight_info):
    carrier = raw_segment.get('marketing_carrier', raw_segment['operating_carrier'])
    segment = Segment.objects.create(
        trip=trip, departure=Airport.objects.get(code=raw_segment['departure']),
        arrival=Airport.objects.get(code=raw_segment['arrival']),
        departure_time=_parse_time(
            raw_segment['departure_date'], raw_segment['departure_time']
        ), arrival_time=_parse_time(
            raw_segment['arrival_date'], raw_segment['arrival_time']
        ), duration=timedelta(minutes=raw_segment['duration']),
        marketing_airline=Airline.objects.get(code=carrier),
        flight=f'{carrier}-{raw_segment["number"]}'
    )
    _create_about(flight_info, raw_segment, segment)


def _parse_travel_time(segments):
    travel_time = 0
    prev = segments[0]
    for curr in segments[1:]:
        travel_time += (_parse_time(
            curr['departure_date'], curr['departure_time']
        ) - _parse_time(prev['arrival_date'], prev['arrival_time'])).total_seconds()
    return travel_time


def _parse_transfer_airports(segments):
    cities = set()
    if len(segments) == 1:
        return cities
    last_i = len(segments) - 1
    for i, segment in enumerate(segments):
        if i > 0:
            cities.add(Airport.objects.get(code=segment['departure']))
        if i < last_i:
            cities.add(Airport.objects.get(code=segment['arrival']))
    return cities


def _parse_trip_duration(segments):
    duration = 0
    prev_segment = None
    for segment in segments:
        duration += segment['duration']
        if prev_segment:
            prev_arrival_time = _parse_time(
                prev_segment['arrival_date'], prev_segment['arrival_time']
            )
            departure_time = _parse_time(
                segment['departure_date'], segment['departure_time']
            )
            duration += int((departure_time - prev_arrival_time).total_seconds()) // 60
        prev_segment = segment
    return timedelta(minutes=duration)


def _create_trips(ticket, query_trips, proposal_trips, flight_info):
    assert len(query_trips) == len(proposal_trips)
    for trip_index, segments in enumerate(proposal_trips):
        query_trip: QueryTrip = query_trips[trip_index]
        trip = Trip.objects.create(
            ticket=ticket, origin=query_trip.origin,
            destination=query_trip.destination,
            start_time=_parse_time(
                segments[0]['departure_date'], segments[0]['departure_time']
            ),
            end_time=_parse_time(
                segments[-1]['arrival_date'], segments[-1]['arrival_time']
            ), transfer_time=_parse_travel_time(segments), number=trip_index,
            duration=_parse_trip_duration(segments)
        )
        trip.transfer_airports.add(*_parse_transfer_airports(segments))
        for segment_index, segment in enumerate(segments):
            _create_segment(trip, segment, flight_info)


def _parse_and_save_results(query, proposals, gates_info, flight_info):
    for proposal in proposals:
        sign = proposal['sign']
        xterms = proposal['xterms']
        try:
            with atomic():
                if ticket := Ticket.objects.filter(sign=sign, query=query).first():
                    _update_offers(gates_info, ticket, xterms)
                    ticket.save()
                    continue
                try:
                    ticket = Ticket.objects.create(sign=sign, query=query)
                except IntegrityError:
                    warning(f'IntegrityError when creating ticket (sign={sign})')
                    raise DatabaseError
                try:
                    best_offer = _create_offers(gates_info, ticket, xterms)
                    ticket.best_offer = best_offer
                    ticket.save()
                    _create_trips(
                        ticket, query.trips.all(), proposal['trips'], flight_info
                    )
                except ObjectDoesNotExist:
                    raise DatabaseError
                except Exception as e:
                    warning(
                        f'{type(e)} when creating data for ticket (sign={sign}): '
                        f'traceback:\n{traceback.format_exc()}'
                    )
                    raise DatabaseError
        except DatabaseError:
            continue


class SearchTicketsService:
    travelpayouts_service = TravelpayoutsService()
    
    DEFAULT_IP = '83.139.179.242'
    host = settings.DOMAIN
    
    def __init__(self, session: TicketsSessionService = None):
        self.session = session
    
    def search(self, query: Query):
        search_id, results = self.__get_results(query)
        proposals = _parse_proposals(results)
        if self.session is not None:
            self.session.search_id = search_id
        gates_info = _parse_gates_info(results)
        flight_info = _parse_flight_info(results)
        _parse_and_save_results(query, proposals, gates_info, flight_info)
    
    def __get_results(self, query: Query) -> tuple[str, list[dict]]:
        ip = self.session.ip if self.session else None
        if not ip or settings.DEBUG and ip == '127.0.0.1':
            ip = self.DEFAULT_IP
        search_id = self.travelpayouts_service.search(
            self.host, ip, [{
                'origin': trip.origin.code,
                'destination': trip.destination.code, 'date': trip.date
            } for trip in query.trips.all()], FlightClass(query.flight_class)
        )
        return search_id, self.travelpayouts_service.search_results(search_id)
