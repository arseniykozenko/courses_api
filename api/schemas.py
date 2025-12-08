"""schemas for pydantic models"""
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """user create schema"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    patronymic: str | None = None


class UserUpdate(BaseModel):
    """user update schema"""
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None


class UserRead(BaseModel):
    """user read schema"""
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    patronymic: str | None
    created_at: datetime

    class Config:
        """config for pydantic"""
        from_attributes = True



class CourseCreate(BaseModel):
    """course create schema"""
    title: str
    description: str | None

class CourseRead(BaseModel):
    """course read schema"""
    id: int
    title: str
    description: str
    created_at: datetime
    
    class Config:
        """config for pydantic"""
        from_attributes = True

class CourseUpdate(BaseModel):
    """course update schema"""
    title: str | None = None
    description: str | None = None

class EnrollmentCreate(BaseModel):
    """enrollment create schema"""
    user_id: int
    course_id: int

class EnrollmentRead(BaseModel):
    """enrollment read schema"""
    id: int
    user_id: int
    course_id: int
    created_at: datetime

    class Config:
        """config for pydantic"""
        from_attributes = True
