"""users service"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.users import UserRepository
from api.schemas import UserCreate, UserUpdate
from utils.models import User
from utils.hashing import hash_password


class UserService:
    """user service"""
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_users(self):
        """get all users"""
        return self.user_repository.get_all()

    def get_user_by_id(self, user_id: int):
        """get user by id"""
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str):
        """get user by email"""
        return self.user_repository.get_by_email(email)

    def create_user(self, user: UserCreate):
        """create user"""
        db_email = self.user_repository.get_by_email(user.email)
        if db_email:
            raise HTTPException(status_code=400, detail="Почта уже существует")
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
        )
        self.user_repository.create_user(new_user)
        return new_user

    def update_user(self, user_id: int, user: UserUpdate):
        """update user"""
        db_user = self.user_repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.patronymic = user.patronymic
        return self.user_repository.update_user(db_user)

    def delete_user(self, user_id: int):
        """delete user"""
        db_user = self.user_repository.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return self.user_repository.delete_user(db_user)
