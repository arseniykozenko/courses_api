import json
from utils.redis import redis_client

TTL_SECONDS = 300

def get_cached_response(request_id: str):
    """
    Возвращает закэшированный ответ, если он есть
    """
    cached = redis_client.get(f"idempotency:{request_id}")
    if cached:
        return json.loads(cached)
    return None


def cache_response(request_id: str, response: dict):
    """
    Сохраняет ответ для идемпотентности
    """
    redis_client.setex(
        f"idempotency:{request_id}",
        TTL_SECONDS,
        json.dumps(response)
    )
