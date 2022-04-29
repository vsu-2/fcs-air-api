from copy import deepcopy
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.utils.translation import get_language
from travelpayouts import Client
from travelpayouts import common
from travelpayouts import flights

from app.air.models.choices import FlightClassChoices
from app.air.services.travelpayouts.types import *
from app.base.exceptions import CriticalError


class TravelpayoutsService(Client):
    BASE_URL = 'https://api.travelpayouts.com'
    
    def __init__(self):
        super().__init__(settings.TRAVELPAYOUTS_TOKEN, str(settings.TRAVELPAYOUTS_MARKER))
    
    def _post(self, url, params=None, json=None):
        full_url = url + '?' + urlencode(params) if params else url
        r = requests.post(full_url, headers=self.default_headers, json=json)
        if not r.ok:
            raise CriticalError(r.json())
        return r.json()
    
    def whereami(self, ip: str) -> WhereamiType:
        return common.whereami(self, ip)
    
    def countries(self, location: str = 'ru') -> list[CountryType]:
        return self._get(f'{common.API_DATA_URL}/{location.lower()}/countries.json')
    
    def cities(self, location: str = 'ru') -> list[CityType]:
        return self._get(f'{common.API_DATA_URL}/{location.lower()}/cities.json')
    
    def airports(self, location: str = 'ru') -> list[AirportType]:
        return self._get(f'{common.API_DATA_URL}/{location.lower()}/airports.json')
    
    def airlines(self, location: str = 'ru') -> list[AirlineType]:
        return self._get(f'{common.API_DATA_URL}/{location.lower()}/airlines.json')
    
    def search(
        self, host: str, user_ip: str, trips: list[TripType],
        flight_class: FlightClassChoices
    ) -> str:
        segments: list = deepcopy(trips)
        for segment in segments:
            segment['date'] = segment['date'].isoformat()
        return flights.search(
            self, segments=segments, passengers={'adults': 1}, currency='rub',
            user_ip=user_ip, host=host, trip_class=flight_class.lower(), locale='ru'
        )['search_id']
    
    def search_results(self, search_id: str) -> list[dict]:
        results = []
        while True:
            result = flights.search_results(self, search_id)
            results.extend(result)
            if result[-1] == {'search_id': search_id}:
                return results[:-1]
            if not result:
                raise CriticalError('search_results пустой')
    
    def get_link(self, url, search_id):
        return flights.get_link(self, url, search_id)['url']
    
    def calendar(self, origin: str, destination: str) -> dict[str, CalendarType]:
        result = self._get(
            'https://api.travelpayouts.com/aviasales/v3/grouped_prices',
            params={
                'origin': origin, 'destination': destination,
                'currency': 'rub', 'group_by': 'departure_at', 'limit': 1000
            }
        )
        return result['data'] or {}
    
    def get_special_offers(
        self, origin: str, destination: str
    ) -> GetSpecialOffersResult | None:
        try:
            return sorted(
                self._get(
                    f'{self.BASE_URL}/aviasales/v3/get_special_offers', params={
                        'locale': 'ru', 'origin': origin,
                        'destination': destination, 'currency': 'rub'
                    }
                )['data'], key=lambda offer: offer['price']
            )[0]
        except IndexError:
            return None
    
    def city_directions(self, origin: str) -> list[str]:
        return list(
            (self._get(
                f'{self.BASE_URL}/v1/city-directions', params={'origin': origin}
            )['data'] or {}).keys()
        )
