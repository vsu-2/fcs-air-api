import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.models import Airport
from app.geo.tests.factories.locations import CityFactory


class AirportFactory(BaseFactory):
    class Meta:
        model = Airport
    
    code = Faker('country_code')
    title = Faker('city')
    city = factory.SubFactory(CityFactory)
