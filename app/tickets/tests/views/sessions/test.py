from unittest import mock

from app.air.models import Query, QueryTrip
from app.air.tests.factiories import QueryTripFactory
from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories import CityFactory
from app.tickets.components.services.search import SearchTicketsService


class TicketsSessionsTest(BaseViewTest):
    path = '/tickets/sessions/'
    
    me_data = None
    
    def test_post__query_already_exists(self):
        query_trip = QueryTripFactory()
        query = query_trip.query
        with mock.patch.object(SearchTicketsService, 'search'):
            self._test(
                'post', {'session_id': lambda sid: isinstance(sid, str)}, {
                    'passengers': query.passengers, 'flight_class': query.flight_class,
                    'trips': [
                        {
                            'origin': query_trip.origin.id,
                            'destination': query_trip.destination.id,
                            'date': query_trip.date
                        }
                    ]
                }
            )
        self.assert_equal(QueryTrip.objects.get(), query_trip)
        self.assert_equal(Query.objects.get(), query)
    
    def test_post__query_does_not_exists(self):
        passengers = fake.random_int(1, 10)
        origin = CityFactory()
        destination = CityFactory()
        date = fake.future_date()
        with mock.patch.object(SearchTicketsService, 'search'):
            self._test(
                'post', {'session_id': lambda sid: isinstance(sid, str)}, {
                    'passengers': passengers, 'trips': [
                        {
                            'origin': origin.id, 'destination': destination.id,
                            'date': date
                        }
                    ]
                }
            )
        self.assert_model(
            QueryTrip, {'origin': origin.id, 'destination': destination.id, 'date': date}
        )
        self.assert_model(Query, {'passengers': passengers})
