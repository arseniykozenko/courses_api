"""enrollments router"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.database import get_db
from api.schemas import EnrollmentResponse, EnrollmentCreate
from services.enrollments import EnrollmentService
from services.courses import CourseService
from services.users import UserService

router = APIRouter(prefix="api/v1/enrollments", tags=["Enrollments"])

get_db()

@router.get("/", response_model=list[EnrollmentResponse])
async def get_enrollments(db: Session = Depends(get_db)):
    """get all enrollments"""
    enrollment_service = EnrollmentService(db)
    try:
        return enrollment_service.get_all_enrollments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить записи на курсы: {e}")

@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """get enrollment by id"""
    enrollment_service = EnrollmentService(db)
    db_enrollment = enrollment_service.get_enrollment_by_id(enrollment_id)
    if not db_enrollment:
        raise HTTPException(404, "Запись на курс не найдена")
    try:
        return db_enrollment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить запись на курс: {e}")

@router.get("/{user_id}", response_model=list[EnrollmentResponse])
async def get_enrollments_by_user(user_id: int, db: Session = Depends(get_db)):
    """get enrollments by user id"""
    enrollment_service = EnrollmentService(db)
    db_enrollments = enrollment_service.get_enrollments_by_user_id(user_id)
    if not db_enrollments:
        raise HTTPException(404, "Записи на курсы для данного пользователя не найдены")
    try:
        return db_enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить записи на курсы: {e}")

@router.get("/{course_id}", response_model=list[EnrollmentResponse])
async def get_enrollments_by_course(course_id: int, db: Session = Depends(get_db)):
    """get enrollments by course id"""
    enrollment_service = EnrollmentService(db)
    db_enrollments = enrollment_service.get_enrollments_by_course_id(course_id)
    if not db_enrollments:
        raise HTTPException(404, "Записи на данный курс не найдены")
    try:
        return db_enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось получить записи на курсы: {e}")

@router.post("/", response_model=EnrollmentResponse)
async def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """create enrollment"""
    enrollment_service = EnrollmentService(db)
    course_service = CourseService(db)
    user_service = UserService(db)
    db_course = course_service.get_course_by_id(enrollment.course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Курс c id {enrollment.course_id} не найден")
    db_user = user_service.get_user_by_id(enrollment.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Пользователь c id {enrollment.user_id} не найден")
    try:
        new_enrollment = enrollment_service.create_enrollment(enrollment)
        return new_enrollment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось создать запись на курс: {e}")


@router.delete("/{enrollment_id}")
async def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """delete enrollment"""
    enrollment_service = EnrollmentService(db)
    db_enrollment = enrollment_service.get_enrollment_by_id(enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Запись на курс не найдена")
    try:
        enrollment_service.delete_enrollment(db_enrollment.id)
        return db_enrollment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось удалить запись на курс: {e}")
