from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin

from app.tickets.components.daos.tickets import TicketsDao
from app.tickets.paginations.sessions import TicketsSessions_SessionId_Pagination
from app.tickets.views.sessions.base import BaseTicketsSessionsView


class TicketsSessions_SessionId_View(ListModelMixin, BaseTicketsSessionsView):
    queryset = TicketsDao().prefetch()
    pagination_class = TicketsSessions_SessionId_Pagination
    filter_backends = BaseTicketsSessionsView.filter_backends + [
        OrderingFilter
    ]
    ordering_fields = ['best_price']
    ordering = 'best_price'
    
    @method_decorator(cache_page(2))
    def get(self, request, **_):
        return self.list(request)
    
    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, self._is_in_progress)
    
    def get_queryset(self):
        return super().get_queryset().filter(query=self.session.query)
