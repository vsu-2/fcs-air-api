from app.air.services.travelpayouts import TravelpayoutsService
from app.base.controllers.base import BaseController
from app.tickets.views import TicketsSessionsDetailOffersDetailLinkView


class GET_TicketsSessionsDetailOffersDetailLinkController(BaseController):
    view: TicketsSessionsDetailOffersDetailLinkView
    travelpayouts_service: TravelpayoutsService
    
    def control(self, data):
        search_id = self.view.session.search_id
        offer = self.view.get_object()
        if not self.view.session.query.tickets.filter(offers=offer.id).exists():
            raise self.view.WARNINGS[423]
        link = self.travelpayouts_service.get_link(offer.url, search_id)
        return {'link': link}
