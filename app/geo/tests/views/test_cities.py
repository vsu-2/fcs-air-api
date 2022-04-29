from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.air import AirportFactory


class CitiesTest(BaseViewTest):
    path = '/geo/cities/'
    
    def test_get_suc(self):
        airport_1 = AirportFactory()
        city = airport_1.city
        country = city.country
        airport_2 = AirportFactory(city=city)
        self._test(
            'get', {
                'count': 1, 'results': [{
                    'id': city.id, 'title': city.title, 'code': city.code,
                    'country': {
                        'id': country.id, 'title': country.title, 'code': country.code
                    },
                    'airports': [
                        {
                            'id': airport_1.id, 'title': airport_1.title,
                            'code': airport_1.code
                        },
                        {
                            'id': airport_2.id, 'title': airport_2.title,
                            'code': airport_2.code
                        }
                    ]
                }]
            }
        )
