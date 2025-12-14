"""Users Router for v2 api"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.v2.schemas import UserCreate, UserUpdate, UserResponse
from utils.database import get_db
from utils.jwt import get_current_user
from utils.rate_limit import rate_limit
from utils.idempotency import idempotency_guard
from utils.redis import redis_client
from services.users import UserService

router = APIRouter(prefix="/api/v2/users", tags=["Users v2"], dependencies=[Depends(get_current_user), Depends(rate_limit)])

get_db()

@router.get("/")
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    fields: str | None = Query(None),
    db: Session = Depends(get_db)
    ):
    """get all users"""
    service = UserService(db)
    try:
        fields_list = fields.split(",") if fields else None
        users = service.get_users(page, size, fields_list)
        if fields_list is None:
            return [UserResponse.model_validate(user) for user in users]
        return users
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
async def create_user(user: UserCreate, db: Session = Depends(get_db), idempotency_key: str = Depends(idempotency_guard)):
    """create user"""
    service = UserService(db)
    db_email = service.get_user_by_email(user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Почта уже существует")
    try:
        new_user = service.create_user(user)
        user_response = UserResponse.model_validate(new_user)
        if idempotency_key:
            key = f"idempotency:{idempotency_key}"
            redis_client.setex(key, 300, user_response.model_dump_json())
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
