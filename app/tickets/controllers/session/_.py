from app.air.components.entities.query import QueryEntity
from app.air.components.factories.query import QueryFactory
from app.base.controllers.base import BaseController


class POST_TicketsSessionController(BaseController):
    query_factory: QueryFactory
    
    dto = QueryEntity
    
    def control(self, data: QueryEntity):
        query = self.query_factory.create(data)
        return {'session_id': str(query)}
