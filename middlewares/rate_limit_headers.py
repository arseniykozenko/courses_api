"""rate limiting middleware"""
from fastapi import Request

async def rate_limit_headers(request: Request, call_next):
    """rate limiting middleware"""
    response = await call_next(request)

    remaining = getattr(request.state, "rate_limit_remaining", None)
    if remaining is not None:
        response.headers["X-Limit-Remaining"] = str(remaining)

    return response
