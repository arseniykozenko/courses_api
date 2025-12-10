"""Enrollment service"""
from repositories.enrollments import EnrollmentRepository
from utils.models import Enrollment
from api.v1.schemas import EnrollmentCreate

class EnrollmentService:
    """Enrollment service class"""
    def __init__(self, db):
        self.enrollment_repository = EnrollmentRepository(db)

    def get_all_enrollments(self):
        """get all enrollments"""
        return self.enrollment_repository.get_all()

    def get_enrollment_by_id(self, enrollment_id: int):
        """get enrollment by id"""
        return self.enrollment_repository.get_by_id(enrollment_id)

    def get_enrollments_by_user_id(self, user_id: int):
        """get enrollments by user id"""
        return self.enrollment_repository.get_enrollments_by_user_id(user_id)

    def get_enrollments_by_course_id(self, course_id: int):
        """get enrollments by course id"""
        return self.enrollment_repository.get_enrollments_by_course_id(course_id)
    
    def create_enrollment(self, enrollment: EnrollmentCreate):
        """create enrollment"""
        new_enrollment = Enrollment(
            user_id=enrollment.user_id,
            course_id=enrollment.course_id
        )
        return self.enrollment_repository.create(new_enrollment)

    def delete_enrollment(self, enrollment_id: int):
        """delete enrollment"""
        db_enrollment = self.enrollment_repository.get_by_id(enrollment_id)
        return self.enrollment_repository.delete(db_enrollment)
