from datetime import datetime, timedelta

from app.air.models import Query, QueryTrip
from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.geo.tests.factories.locations import CityFactory


class TicketsSessionTest(BaseViewTest):
    path = '/tickets/session/'
    
    me_data = None
    
    def test_post(self):
        passengers = fake.random_int(1, 10)
        origin = CityFactory()
        destination = CityFactory()
        date = fake.future_date(datetime.now() + timedelta(days=330))
        session_id = fake.random_string()
        self._test(
            'post', {'session_id': lambda sid: isinstance(sid, str)}, {
                'passengers': passengers,
                'trips': [
                    {'origin': origin.id, 'destination': destination.id, 'date': date}
                ]
            }
        )
        query = self.assert_model(Query, {'passengers': passengers})
        self.assert_model(
            QueryTrip, {
                'query': query.id, 'origin': origin.id, 'destination': destination.id,
                'date': date
            }
        )
