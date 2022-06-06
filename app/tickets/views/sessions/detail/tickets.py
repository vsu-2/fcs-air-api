from rest_framework.mixins import ListModelMixin

from app.tickets.components.daos.tickets import TicketsDao
from app.tickets.filters.sessions import TicketsSessionsDetailTicketsFilter
from app.tickets.paginations.sessions import TicketsSessions_SessionId_Pagination
from app.tickets.views.sessions.detail.base import BaseTicketsSessionsDetailView


class TicketsSessionsDetailTicketsView(ListModelMixin, BaseTicketsSessionsDetailView):
    queryset = TicketsDao().prefetch().order_by('best_offer__price')
    pagination_class = TicketsSessions_SessionId_Pagination
    filterset_class = TicketsSessionsDetailTicketsFilter
    
    def get(self, request, **_):
        return self.list(request)
    
    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, self.is_in_progress)
    
    def get_queryset(self):
        return super().get_queryset().filter(query=self.session.query)
