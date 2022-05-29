from __future__ import annotations

from django.utils.crypto import get_random_string

from app.air.models import Query
from app.base.services.cache.cache import BaseCacheService


class TicketsSessionService(BaseCacheService):
    SCOPE = 'tickets'
    TIMEOUT = 60 * 10
    DEFAULT = None
    
    def __init__(self, id: str):
        self.id = id
    
    @classmethod
    def create(cls) -> TicketsSessionService:
        session_id = get_random_string(10)
        return TicketsSessionService(session_id)
    
    @property
    def task_id(self) -> str:
        return self.get(self.id, 'task_id')
    
    @task_id.setter
    def task_id(self, task_id):
        self.set(task_id, self.id, 'task_id')
    
    @property
    def search_id(self) -> str:
        return self.get(self.id, 'search_id')
    
    @search_id.setter
    def search_id(self, search_id):
        self.set(search_id, self.id, 'search_id')
    
    @property
    def ip(self) -> str | None:
        return self.get(self.id, 'ip')
    
    @ip.setter
    def ip(self, ip):
        self.set(ip, self.id, 'ip')
    
    @property
    def query(self) -> Query:
        return self.get(self.id, 'query')
    
    @query.setter
    def query(self, query):
        self.set(query, self.id, 'query')
