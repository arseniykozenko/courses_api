"""auth util for internal api"""
import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")

def verify_internal_key(
    x_internal_key: str = Header(..., alias="X-Internal-Key"),
):
    """verify internal key"""
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Internal access only",
        )
