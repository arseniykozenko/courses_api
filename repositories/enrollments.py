"""Enrollments repository"""
from sqlalchemy.orm import Session
from utils import models

class EnrollmentRepository:
    """repository for enrollments"""
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, enrollment_id: int):
        """get enrollment by id"""
        return self.db.query(models.Enrollment).filter(models.Enrollment.id == enrollment_id).first()

    def get_all(self):
        """get all enrollments"""
        return self.db.query(models.Enrollment).all()
    
    def get_enrollments_by_user_id(self, user_id: int):
        """get enrollments by user id"""
        return self.db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id).all()

    def get_enrollments_by_course_id(self, course_id: int):
        """get enrollments by course id"""
        return self.db.query(models.Enrollment).filter(models.Enrollment.course_id == course_id).all()

    def create(self, enrollment: models.Enrollment):
        """create enrollment"""
        try:
            self.db.add(enrollment)
            self.db.commit()
            self.db.refresh(enrollment)
            return enrollment
        except Exception: # pylint: disable=broad-except
            self.db.rollback()
            return None

    def delete(self, enrollment: models.Enrollment):
        """delete enrollment"""
        try:
            self.db.delete(enrollment)
            self.db.commit()
            return enrollment
        except Exception: # pylint: disable=broad-except
            self.db.rollback()
            return False
