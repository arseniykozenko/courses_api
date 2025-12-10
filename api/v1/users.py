"""Users Router for v1 api"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas import UserCreate, UserResponse, UserUpdate
from utils.database import get_db
from services.users import UserService


router = APIRouter(prefix="api/v1/users", tags=["Users"])

get_db()

@router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """get all users"""
    service = UserService(db)
    try:
        return service.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить пользователей: {e}")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """get user by id"""
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    try:
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить пользователя: {e}")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """create user"""
    service = UserService(db)
    db_email = service.get_user_by_email(user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Почта уже существует")
    try:
        new_user = service.create_user(user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать пользователя: {e}")


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """update user"""
    service = UserService(db)
    db_user = service.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    try:
        db_user = service.update_user(user_id, user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось обновить пользователя: {e}")


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """delete user"""
    service = UserService(db)
    db_user = service.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    try:
        service.delete_user(db_user.id)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось удалить пользователя: {e}")
