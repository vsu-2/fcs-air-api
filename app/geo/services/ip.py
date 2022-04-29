from __future__ import annotations


class IpService:
    def __init__(self, ip: str):
        self.ip: str = ip
    
    @classmethod
    def from_request(cls, request) -> IpService | None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip is None:
            return None
        return IpService(ip)
