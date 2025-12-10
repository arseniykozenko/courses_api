"""Auth Router for v2 api"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.v2.schemas import UserCreate, UserResponse, UserLoginResponse, UserLogin
from utils.database import get_db
from utils.hashing import verify_password
from utils.jwt import create_access_token
from services.users import UserService


router = APIRouter(prefix="/api/v2/auth", tags=["Auth v2"])

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
    

@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """login user"""
    service = UserService(db)
    db_user = service.authenticate_user(user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    access_token = create_access_token(data={"sub": db_user.email})
    try:
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось залогинить пользователя: {e}")
