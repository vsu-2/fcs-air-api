import factory

from app.base.tests.factories.base import BaseFactory
from app.geo.models import Airport
from app.geo.tests.factories.locations import CityFactory


class AirportFactory(BaseFactory):
    class Meta:
        model = Airport
    
    code = factory.Faker('country_code')
    title = factory.Faker('city')
    city = factory.SubFactory(CityFactory)
