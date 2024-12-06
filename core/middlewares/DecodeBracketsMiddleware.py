from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class DecodeBracketsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        new_scope = dict(request.scope)
        query_bytes: bytes = request.scope['query_string']
        query_string: str = query_bytes.decode('utf-8')
        decoded_query_string = query_string.replace('%5B%5D', '[]')
        new_scope['query_string'] = decoded_query_string.encode('utf-8')
        
        request = Request(new_scope, request.receive)
        return await call_next(request)