from rest_framework import serializers

from app.geo.models import *
from app.tickets.models import *


class _GET_TicketsSessionsDetailTickets__BestOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'gate_id', 'title', 'price']


class \
    _GET_TicketsSessionsDetailTickets__Trips__Segments__Departure_Arrival__CitySerializer(
    # noqa
    serializers.ModelSerializer
):
    class Meta:
        model = City
        fields = ['id', 'code', 'title']


class _GET_TicketsSessionsDetailTickets__Trips__Segments__Departure_ArrivalSerializer(
    serializers.ModelSerializer
):
    city = \
        _GET_TicketsSessionsDetailTickets__Trips__Segments__Departure_Arrival__CitySerializer()  # noqa
    
    class Meta:
        model = Airport
        fields = ['id', 'code', 'title', 'city']


class _GET_TicketsSessionsDetailTickets__Trips__Segments__MarketingAirlineSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Airline
        fields = ['id', 'code', 'title']


class _GET_TicketsSessionsDetailTickets__Trips__SegmentsSerializer(
    serializers.ModelSerializer
):
    departure = \
        _GET_TicketsSessionsDetailTickets__Trips__Segments__Departure_ArrivalSerializer()
    arrival = \
        _GET_TicketsSessionsDetailTickets__Trips__Segments__Departure_ArrivalSerializer()
    marketing_airline = \
        _GET_TicketsSessionsDetailTickets__Trips__Segments__MarketingAirlineSerializer()
    
    class Meta:
        model = Segment
        fields = [
            'id', 'departure', 'arrival', 'departure_time', 'arrival_time', 'duration',
            'marketing_airline', 'flight'
        ]


class _GET_TicketsSessionsDetailTickets__TripsSerializer(serializers.ModelSerializer):
    segments = _GET_TicketsSessionsDetailTickets__Trips__SegmentsSerializer(many=True)
    
    class Meta:
        model = Trip
        fields = ['start_time', 'end_time', 'segments']


class GET_TicketsSessionsDetailTicketsSerializer(serializers.ModelSerializer):
    best_offer = _GET_TicketsSessionsDetailTickets__BestOfferSerializer()
    trips = _GET_TicketsSessionsDetailTickets__TripsSerializer(many=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'best_offer', 'trips']
