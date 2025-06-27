import time, logging
from functools import wraps
from flask import g, request, current_app as app

_log = logging.getLogger("timings")

def before() -> None:
    g.__start = time.perf_counter()

def after(response):
    # guard for blueprints or static files that skip before()
    if hasattr(g, "__start"):
        ms = (time.perf_counter() - g.__start) * 1000
        _log.info("%s %s %.2f ms", request.method, request.path, ms)
        response.headers["X-Response-Time"] = f"{ms:.2f} ms"
    return response

def timed(view):
    """Decorate an individual view if you don’t want global hooks."""
    @wraps(view)
    def wrapper(*a, **kw):
        g.__start = time.perf_counter()
        resp = view(*a, **kw)
        return after(resp)
    return wrapper
