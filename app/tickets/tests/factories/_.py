import factory

from app.air.tests.factiories import QueryFactory
from app.base.tests.factories.base import BaseFactory
from app.base.tests.fakers import Faker
from app.geo.tests.factories import AirlineFactory
from app.geo.tests.factories.locations import CityFactory
from app.tickets.models import *


class TicketFactory(BaseFactory):
    query = factory.SubFactory(QueryFactory)
    sign = Faker('uuid4')
    
    class Meta:
        model = Ticket
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        ticket = super()._create(model_class, *args, **kwargs)
        ticket.best_offer = OfferFactory()
        return ticket


class TripFactory(BaseFactory):
    ticket = factory.SubFactory(TicketFactory)
    origin = factory.SubFactory(CityFactory)
    destination = factory.SubFactory(CityFactory)
    number = Faker('random_int', max=5)
    start_time = Faker('future_datetime')
    end_time = Faker('future_datetime')
    
    class Meta:
        model = Trip


class OfferFactory(BaseFactory):
    ticket = factory.SubFactory(TicketFactory)
    gate_id = Faker('random_int', max=100)
    title = Faker('company')
    price = Faker('pyfloat', min_value=1)
    url = Faker('random_int', max=100)
    
    class Meta:
        model = Offer


class SegmentFactory(BaseFactory):
    trip = factory.SubFactory(TripFactory)
    departure = factory.SubFactory(CityFactory)
    arrival = factory.SubFactory(CityFactory)
    marketing_airline = factory.SubFactory(AirlineFactory)
    departure_time = Faker('future_datetime')
    arrival_time = Faker('future_datetime')
    duration = Faker('time_delta')
    flight = Faker('pystr')
    
    class Meta:
        model = Segment


class AboutFactory(BaseFactory):
    segment = factory.SubFactory(SegmentFactory)
    airline = factory.SubFactory(AirlineFactory)
    
    class Meta:
        model = About
