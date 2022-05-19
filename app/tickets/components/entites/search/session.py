from app.base.services.cache.cache import BaseCacheService


class SearchSessionService(BaseCacheService):
    SCOPE = 'tickets'
    TIMEOUT = 60 * 10
    DEFAULT = None
    
    def __init__(self, id: str):
        self.id = id
    
    @classmethod
    def create(cls) -> SearchSessionService:
        session_id = get_random_string(10)
        return SearchSessionService(session_id)
    
    @property
    def task_id(self) -> str | None:
        return self.get(self.id, 'task_id')
    
    @task_id.setter
    def task_id(self, task_id):
        self.set(task_id, self.id, 'task_id')
    
    @property
    def search_id(self) -> str | None:
        return self.get(self.id, 'search_id')
    
    @search_id.setter
    def search_id(self, search_id):
        self.set(search_id, self.id, 'search_id')
    
    @property
    def query(self) -> AirQuery | None:
        return self.get(self.id, 'query')
    
    @query.setter
    def query(self, query):
        self.set(query, self.id, 'query')
