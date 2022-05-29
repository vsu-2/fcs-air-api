from app.air.components.entities.query import QueryEntity
from app.air.components.managers.query import QueryManager
from app.base.controllers.base import BaseController
from app.tickets.components.services.session import TicketsSessionService
from app.tickets.tasks import search_tickets


class POST_TicketsSessionController(BaseController):
    query_manager: QueryManager
    
    dto = QueryEntity
    
    def control(self, data: QueryEntity):
        query = self.query_manager.create(data)
        session = TicketsSessionService.create()
        session.query = query
        session.task_id = search_tickets.delay(session.id).id
        return {'session_id': session.id}
