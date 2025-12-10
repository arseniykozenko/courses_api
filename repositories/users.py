"""users repository"""
from sqlalchemy.orm import Session
from utils import models

class UserRepository:
    """user repository class"""
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        """get all users"""
        return self.db.query(models.User).all()
    
    def get_by_id(self, user_id: int):
        """get user by id"""
        return self.db.query(models.User).filter(models.User.id == user_id).first()
    
    def get_by_email(self, email: str):
        """get user by email"""
        return self.db.query(models.User).filter(models.User.email == email).first()
        
    def create_user(self, user: models.User):
        """create user"""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            print(f"Failed to create user: {e}")
            return None

    def update_user(self, user: models.User):
        """update user"""
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            print(f"Failed to update user: {e}")
            return None

    def delete_user(self, user: models.User):
        """delete user"""
        try:
            self.db.delete(user)
            self.db.commit()
            return user
        except Exception as e:
            self.db.rollback()
            print(f"Failed to delete user: {e}")
