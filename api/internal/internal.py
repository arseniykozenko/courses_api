"""internal api router"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.internal_auth import verify_internal_key
from services.courses import CourseService

router = APIRouter(
    prefix="/internal/courses",
    tags=["Internal"],
    dependencies=[Depends(verify_internal_key)],
    include_in_schema=False,
)

get_db()

@router.get("/")
def get_all_courses_internal(db: Session = Depends(get_db)):
    """
    Internal endpoint: get all courses without pagination:
    curl http://localhost:8080/internal/courses/ -H "X-Internal-Key: secret-internal-key"
    """
    service = CourseService(db)
    return service.get_all_courses_internal()
