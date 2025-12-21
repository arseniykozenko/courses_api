"""auth api key utils"""
VALID_API_KEYS = {
    "API_KEY_123",
    "API_KEY_456"
}

def check_api_key(api_key: str) -> bool:
    return api_key in VALID_API_KEYS