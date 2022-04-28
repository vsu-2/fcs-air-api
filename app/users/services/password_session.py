from django.core.cache import cache
from django.utils.crypto import get_random_string


class PasswordSessionService:
    SESSION_LENGTH: int = 10
    SESSION_EXPIRE: int = 3600
    SESSION_PREFIX: str = 'password_session'
    
    def create(self, email: str) -> str:
        session_id = get_random_string(self.SESSION_LENGTH)
        key = f'{self.SESSION_PREFIX}:{session_id}'
        cache.set(key, email, self.SESSION_EXPIRE)
        return session_id
    
    def check(self, session: str) -> str | None:
        key = f'{self.SESSION_PREFIX}:{session}'
        email = cache.get(key)
        if email is None:
            return None
        cache.delete(key)
        return email
