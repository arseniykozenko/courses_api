"""courses router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.database import get_db
from api.schemas import CourseResponse, CourseCreate, CourseUpdate
from services.courses import CourseService

router = APIRouter(prefix="api/v1/courses", tags=["Courses"])

get_db()

@router.get("/", response_model=list[CourseResponse])
async def get_courses(db: Session = Depends(get_db)):
    """get all courses"""
    course_service = CourseService(db)
    try:
        return course_service.get_all_courses()
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
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """create course"""
    course_service = CourseService(db)
    try:
        new_course = course_service.create_course(course)
        return new_course
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать курс: {e}")

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
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
