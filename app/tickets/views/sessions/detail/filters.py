from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from app.tickets.views.sessions.detail.base import BaseTicketsSessionsDetailView


def _map_trips_by_number(queryset, lookup):
    non_order_lookup = lookup[1:] if lookup.startswith('-') else lookup
    return queryset.order_by('number', lookup).distinct('number').values_list(
        non_order_lookup, flat=True
    )


class TicketsSessionsDetailFiltersView(BaseTicketsSessionsDetailView):
    ticket_ids: list[int]
    
    @method_decorator(cache_page(2))
    def get(self, request, **_):
        return self.handle()
