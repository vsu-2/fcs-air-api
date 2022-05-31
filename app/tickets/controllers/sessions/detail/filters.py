from django.db.models import Count, F, Max, Min, Q

from app.base.controllers.base import BaseController
from app.geo.models import *
from app.tickets.models import *
from app.tickets.views.sessions.detail.filters import TicketsSessionsDetailFiltersView


class GET_TicketsSessionsDetailFiltersController(BaseController):
    view: TicketsSessionsDetailFiltersView
    ticket_ids: list[int]
    
    def control(self, data):
        query = self.view.session.query
        self.ticket_ids = list(
            Ticket.objects.filter(query=query).values_list('id', flat=True)
        )
        return {
            'in_progress': self.view.is_in_progress,
            'transfers': self._get_transfers(),
            'travel_time_range': self._get_travel_time_range(),
            'airlines': self._get_airlines(),
            'airports': self._get_airports(),
            'offers': self._get_offers(),
            'best_price': self._get_best_price()
        }
    
    def _get_transfers(self):
        transfers = set(
            Trip.objects.filter(ticket__in=self.ticket_ids).annotate(
                Count('segments')
            ).values_list('segments__count', flat=True)
        )
        return [transfer - 1 for transfer in transfers if transfer]
    
    def _get_travel_time_range(self):
        return Ticket.objects.filter(id__in=self.ticket_ids).aggregate(
            min=Min('travel_time'), max=Max('travel_time')
        )
    
    def _get_airlines(self):
        return Airline.objects.filter(
            abouts__segment__trip__ticket__in=self.ticket_ids
        ).distinct()
    
    def _get_airports(self):
        return Airport.objects.filter(
            Q(segments_by_arrival__trip__ticket__in=self.ticket_ids) |
            Q(segments_by_departure__trip__ticket__in=self.ticket_ids)
        ).distinct()
    
    def _get_offers(self):
        return sorted(
            Offer.objects.filter(
                tickets_by_best_offer__in=self.ticket_ids
            ).order_by('gate_id', 'price').distinct('gate_id'), key=lambda o: o.price
        )
    
    def _get_best_price(self):
        best_ticket = Ticket.objects.filter(id__in=self.ticket_ids).annotate(
            best_price=F(f'best_offer__price')
        ).order_by('best_price').first()
        return None if best_ticket is None else best_ticket.best_price
