import warnings

from django.core.management.base import BaseCommand
from django.db.models import Count

from app.air.services.travelpayouts import TravelpayoutsService
from app.geo.models import Country, City, Airport, Airline


def _update_or_create(model, code, data):
    try:
        instance = model.objects.get(code=code)
    except model.DoesNotExist:
        instance = model(code=code)
    [setattr(instance, key, value) for key, value in data.items()]
    instance.save()


def _percentages(prefix, i, size):
    percent = i / (size // 10)
    if percent.is_integer():
        print(f'{prefix}: {int(percent * 10)}%')


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.service = TravelpayoutsService()
    
    def handle(self, *args, **options):
        imports = [
            k for k, v in options.items() if
            k in ('country', 'city', 'airport', 'airline') and v
        ]
        if not imports:
            self._import_countries()
            self._import_cites()
            self._import_airports()
            self._import_airlines()
        else:
            if 'country' in imports:
                self._import_countries()
            if 'city' in imports:
                self._import_cites()
            if 'airport' in imports:
                self._import_airports()
            if 'airline' in imports:
                self._import_airlines()
        City.objects.annotate(Count('airport')).filter(airport__count=0).delete()
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--country', action='store_true', default=False, help='Импорт только стран'
        )
        parser.add_argument(
            '--city', action='store_true', default=False, help='Импорт только городов'
        )
        parser.add_argument(
            '--airport', action='store_true', default=False,
            help='Импорт только аэропортов'
        )
        parser.add_argument(
            '--airline', action='store_true', default=False,
            help='Импорт только авиакомпаний'
        )
    
    def _import_countries(self):
        countries = self.service.countries()
        country_data: dict
        for i, country_data in enumerate(countries):
            _percentages('countries', i, len(countries))
            _update_or_create(Country, country_data.pop('code'), country_data['name'])
    
    def _import_cites(self):
        cities = self.service.cities()
        city_data: dict
        for i, city_data in enumerate(cities):
            _percentages('cities', i, len(cities))
            country = Country.objects.get(code=city_data.pop('country_code'))
            _update_or_create(
                City, city_data.pop('code'), city_data | {'country': country}
            )
    
    def _import_airports(self):
        airports = self.service.airports()
        airport_data: dict
        for i, airport_data in enumerate(airports):
            _percentages('airports', i, len(airports))
            city_code = airport_data.pop('city_code')
            airport_code = airport_data.pop('code')
            try:
                city = City.objects.get(code=city_code)
                _update_or_create(Airport, airport_code, airport_data | {'city': city})
            except City.DoesNotExist:
                warnings.warn(
                    f'Для аэропорта {airport_data} с кодом {airport_code} указан '
                    f'некорректный код города: {city_code}'
                )
    
    def _import_airlines(self):
        airlines = self.service.airlines()
        airline_data: dict
        for i, airline_data in enumerate(airlines):
            _percentages('airlines', i, len(airlines))
            _update_or_create(Airline, airline_data.pop('code'), airline_data)
