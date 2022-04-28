from typing import Protocol


class FakeProtocol(Protocol):
    def email(self) -> str:
        pass
    
    def password(self) -> str:
        pass
    
    def first_name(self) -> str:
        pass
    
    def last_name(self) -> str:
        pass
