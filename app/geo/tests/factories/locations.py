import factory

from app.base.tests.factories.base import BaseFactory
from app.geo.models import City, Country


class CountryFactory(BaseFactory):
    class Meta:
        model = Country
    
    code = factory.Faker('country_code')
    title = factory.Faker('city')


class CityFactory(BaseFactory):
    class Meta:
        model = City
    
    code = factory.Faker('country_code')
    title = factory.Faker('city')
    country = factory.SubFactory(CountryFactory)
