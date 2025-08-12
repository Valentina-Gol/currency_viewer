from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
from time import time
from logging import getLogger
from app.middleware.context_utils import set_request_id


_log = getLogger(__name__)



class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        set_request_id(request_id)
        _log.info("[%s] %s %s started" % (request_id, request.method, request.url.path))
        t0 = time()
        response = await call_next(request)
        t1 = time()
        _log.info("[%s] %s %s [elapsed time: %.3fs]" % (request_id, request.method, request.url.path, t1 - t0))
        return response
