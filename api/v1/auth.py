"""Auth Router for v1 api"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v1.schemas import UserCreate, UserResponse
from utils.database import get_db
from services.users import UserService


router = APIRouter(prefix="/api/v1/auth", tags=["Auth v1"])

get_db()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """register user"""
    service = UserService(db)
    db_email = service.get_user_by_email(user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Почта уже существует")
    try:
        new_user = service.create_user(user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось зарегистрировать пользователя: {e}")