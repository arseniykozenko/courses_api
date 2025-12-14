"""courses service"""
from repositories.courses import CourseRepository
from utils.models import Course
from api.v1.schemas import CourseCreate, CourseUpdate

class CourseService:
    """course service class"""
    def __init__(self, db):
        self.course_repository = CourseRepository(db)
    
    def get_all_courses_internal(self):
        """get all courses without pagination, for internal use only"""
        return self.course_repository.get_all_raw()

    def get_all_courses(self, page: int, size: int, fields: list[str] | None = None):
        """get all courses"""
        offset = (page - 1) * size
        courses = self.course_repository.get_all(offset, size)
        if not fields:
            return courses
        allowed = {'id', 'title', 'description', 'created_at', 'updated_at'}
        fields = set(fields) & allowed
        result = []
        for course in courses:
            result.append({field: getattr(course, field) for field in fields})
        return result
    
    def get_course_by_title(self, title: str):
        """get course by title"""
        return self.course_repository.get_by_title(title)

    def get_course_by_id(self, course_id: int):
        """get course by id"""
        return self.course_repository.get_by_id(course_id)

    def create_course(self, course: CourseCreate):
        """create course"""
        new_course = Course(
            title=course.title, 
            description=course.description
        )
        return self.course_repository.create(new_course)
    def update_course(self, course_id: int, course: CourseUpdate):
        """update course"""
        db_course = self.course_repository.get_by_id(course_id)
        if course.title is not None:
            db_course.title = course.title
        if course.description is not None:
            db_course.description = course.description

        return self.course_repository.update(db_course)

    def delete_course(self, course_id: int):
        """delete course"""
        db_course = self.course_repository.get_by_id(course_id)
        return self.course_repository.delete(db_course)
