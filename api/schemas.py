"""schemas for pydantic models"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    """user base schema"""
    email: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None


class UserCreate(UserBase):
    """user create schema"""
    password: str

class UserUpdate(BaseModel):
    """user update schema"""
    first_name: str
    last_name: str
    patronymic: Optional[str] = None


class UserResponse(UserBase):
    """user response schema"""
    id: int
    created_at: datetime

    class Config:
        """config for pydantic"""
        from_attributes = True

class CourseBase(BaseModel):
    """course base schema"""
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    """course create schema"""
    pass


class CourseUpdate(BaseModel):
    """course update schema"""
    title: Optional[str] = None
    description: Optional[str] = None


class CourseResponse(CourseBase):
    """course response schema"""
    id: int
    created_at: datetime

    class Config:
        """config for pydantic"""
        from_attributes = True

class EnrollmentCreate(BaseModel):
    """enrollment create schema"""
    user_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    """enrollment response schema"""
    id: int
    user_id: int
    course_id: int
    created_at: datetime

    class Config:
        """config for pydantic"""
        from_attributes = True
