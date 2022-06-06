from app.tickets.views.sessions.detail.base import BaseTicketsSessionsDetailView


def _map_trips_by_number(queryset, lookup):
    non_order_lookup = lookup[1:] if lookup.startswith('-') else lookup
    return queryset.order_by('number', lookup).distinct('number').values_list(
        non_order_lookup, flat=True
    )


class TicketsSessionsDetailFiltersView(BaseTicketsSessionsDetailView):
    ticket_ids: list[int]
    
    def get(self, request, **_):
        return self.handle()
