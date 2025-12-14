"""courses router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.jwt import get_current_user
from utils.rate_limit import rate_limit
from utils.idempotency import idempotency_guard
from utils.redis import redis_client
from api.v2.schemas import CourseResponse, CourseCreate, CourseUpdate
from services.courses import CourseService


router = APIRouter(prefix="/api/v2/courses", tags=["Courses v2"], dependencies=[Depends(get_current_user), Depends(rate_limit)])

get_db()

@router.get("/", response_model=list[CourseResponse])
async def get_courses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    ):
    """get all courses"""
    course_service = CourseService(db)
    try:
        courses = course_service.get_all_courses(page, size)
        return [CourseResponse.model_validate(course) for course in courses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить курсы: {e}")

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """get course by id"""
    course_service = CourseService(db)
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    try:
        return course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить курс: {e}")



@router.post("/", response_model=CourseResponse)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    idempotency_key: str = Depends(idempotency_guard)
    ):
    """create course"""
    course_service = CourseService(db)
    try:
        new_course = course_service.create_course(course)
        course_response = CourseResponse.model_validate(new_course)
        if idempotency_key:
            key = f"idempotency:{idempotency_key}"
            redis_client.setex(key, 300, course_response.model_dump_json())
        return new_course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать курс: {e}")

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    """update course"""
    course_service = CourseService(db)
    db_course = course_service.get_course_by_id(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    try:
        db_course = course_service.update_course(course_id, course)
        return db_course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось обновить курс: {e}")


@router.delete("/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    """delete course"""
    course_service = CourseService(db)
    db_course = course_service.get_course_by_id(course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    try:
        course_service.delete_course(db_course.id)
        return db_course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось удалить курс: {e}")
