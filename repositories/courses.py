"""courses repository"""
from sqlalchemy.orm import Session
from utils import models

class CourseRepository:
    """courses repository class"""
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, course_id: int):
        """get course by id"""
        return self.db.query(models.Course).filter(models.Course.id == course_id).first()
    
    def get_by_title(self, title: str):
        """get course by title"""
        return self.db.query(models.Course).filter(models.Course.title == title).first()

    def get_all(self):
        """get all courses"""
        return self.db.query(models.Course).all()

    def create(self, course: models.Course):
        """create course"""
        try:
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e: # pylint: disable=broad-except
            self.db.rollback()
            print(f"Failed to create course: {e}")
            return None

    def update(self, course: models.Course):
        """update course"""
        try:
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception: # pylint: disable=broad-except
            self.db.rollback()
            return None

    def delete(self, course: models.Course):
        """delete course"""
        try:
            self.db.delete(course)
            self.db.commit()
            return course
        except Exception: # pylint: disable=broad-except
            self.db.rollback()
            return False
