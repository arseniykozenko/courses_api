"""rate limit util"""
from fastapi import Request, HTTPException
from utils.redis import redis_client

RATE_LIMIT = 20
RATE_LIMIT_WINDOW = 60

async def rate_limit(request: Request):
    """
    Ограничение частоты запросов
    """

    user = request.state.user if hasattr(request.state, "user") else None
    client_id = f"user:{user.id}" if user else f"ip:{request.client.host}"

    key = f"rate_limit:{client_id}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, RATE_LIMIT_WINDOW)

    remaining = RATE_LIMIT - current
    ttl = redis_client.ttl(key)

    if current > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={
                "Retry-After": str(ttl),
                "X-Limit-Remaining": "0",
            }
        )

    request.state.rate_limit_remaining = max(0, remaining)
