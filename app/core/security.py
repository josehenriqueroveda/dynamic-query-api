from slowapi import Limiter
from slowapi.util import get_remote_address


class RequestLimiter:
    def __init__(self):
        self.limiter = Limiter(key_func=get_remote_address)

    def get_limiter(self):
        return self.limiter


request_limiter = RequestLimiter()
