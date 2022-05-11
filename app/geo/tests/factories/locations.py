import factory

from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.models import City, Country


class CountryFactory(BaseFactory):
    class Meta:
        model = Country
    
    code = Faker('country_code')
    title = Faker('city')


class CityFactory(BaseFactory):
    class Meta:
        model = City
    
    code = Faker('country_code')
    title = Faker('city')
    country = factory.SubFactory(CountryFactory)
