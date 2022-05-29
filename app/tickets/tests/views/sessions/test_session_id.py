from unittest import mock

from app.base.tests.fakers import fake
from app.base.tests.views.base import BaseViewTest
from app.tickets.components.services.session import TicketsSessionService
from app.tickets.tests.factories import AboutFactory


class TicketsSessions_SessionId_Test(BaseViewTest):
    _session_id: str = fake.random_string()
    
    @property
    def path(self):
        return f'/tickets/sessions/{self._session_id}/'
    
    me_data = None
    
    def test_get(self):
        query = AboutFactory().segment.trip.ticket.query
        with mock.patch.object(
            TicketsSessionService, 'query', mock.PropertyMock(return_value=query)
        ), mock.patch.object(
            TicketsSessionService, 'task_id',
            mock.PropertyMock(return_value=fake.random_string())
        ):
            self._test('get', {'count': 1})
