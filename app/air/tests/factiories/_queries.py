import factory

from app.air.models import *
from app.air.models.choices import FlightClass
from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.tests.factories.locations import CityFactory


class QueryFactory(BaseFactory):
    passengers = Faker('random_int', min=1, max=10)
    flight_class = factory.Iterator(FlightClass)
    
    class Meta:
        model = Query


class QueryTripFactory(BaseFactory):
    query = factory.SubFactory(QueryFactory)
    origin = factory.SubFactory(CityFactory)
    destination = factory.SubFactory(CityFactory)
    date = Faker('future_date')
    
    class Meta:
        model = QueryTrip
