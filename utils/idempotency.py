"""idempotency util"""
import json
from fastapi import Header, HTTPException
from utils.redis import redis_client

async def idempotency_guard(
    idempotency_key: str = Header(alias="Idempotency-Key"),
):
    """idempotency guard"""
    if not idempotency_key:
        return None

    if len(idempotency_key) > 255:
        raise HTTPException(
            status_code=400,
            detail="Idempotency key is too long"
        )
    if not idempotency_key.strip():
        raise HTTPException(
            status_code=400,
            detail="Idempotency key is empty"
        )

    key = f"idempotency:{idempotency_key}"

    cached = redis_client.get(key)
    if cached:
        data = json.loads(cached)
        raise HTTPException(
            status_code=200,
            detail=data
        )
     
    return idempotency_key