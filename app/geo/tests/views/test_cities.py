from parameterized import parameterized

from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.air import AirportFactory
from app.geo.tests.factories.locations import CityFactory


class CitiesTest(BaseViewTest):
    path = '/geo/cities/'
    
    def test_get(self):
        AirportFactory()
        self._test('get', {'count': 1})
    
    @parameterized.expand([['моск', 2], ['дом', 1], ['ш', 1], ['воронеж', 0]])
    def test_filters(self, title, count):
        AirportFactory(title='Домодедово', city=CityFactory(title='Москва'))
        AirportFactory(title='Шереметьево', city=CityFactory(title='Москва'))
        self._test('get', {'count': count}, data={'title__icontains': title})
