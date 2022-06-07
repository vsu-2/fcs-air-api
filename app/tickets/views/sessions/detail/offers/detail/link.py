from app.base.exceptions import APIWarning
from app.tickets.models import Offer
from app.tickets.views.sessions.detail.base import BaseTicketsSessionsDetailView


class TicketsSessionsDetailOffersDetailLinkView(BaseTicketsSessionsDetailView):
    WARNINGS = BaseTicketsSessionsDetailView.WARNINGS | {
        423: APIWarning(
            'Этот offer недоступен в данной сессии (его нет в выдаче)', 423,
            'offer_locked'
        )
    }
    
    queryset = Offer.objects.all()
    lookup_url_kwarg = 'offer_id'
    
    def get(self, request, **_):
        return self.handle()
