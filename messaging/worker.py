import json
import logging
import pika
from datetime import datetime

from messaging.rabbitmq import channel
from messaging.queues import REQUEST_QUEUE, DLQ_QUEUE

from utils.auth import check_api_key
from utils.idempotency import get_cached_response, cache_response
from utils.database import get_db

from services.users import UserService
from services.courses import CourseService
from services.enrollments import EnrollmentService

from api.v1.schemas import UserResponse as UserResponseV1, CourseResponse as CourseResponseV1, EnrollmentResponse as EnrollmentResponseV1
from api.v2.schemas import (
    UserCreate, UserUpdate, UserResponse as UserResponseV2,
    CourseCreate, CourseUpdate, CourseResponse as CourseResponseV2,
    EnrollmentCreate, EnrollmentResponse as EnrollmentResponseV2
)

# -------------------- RESPONSE --------------------
def serialize(obj):
    """Преобразуем объекты в JSON-сериализуемые"""
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("worker.log"),
        logging.StreamHandler()
    ]
)

MAX_RETRIES = 3
RETRY_DELAY = 5

def send_response(properties, correlation_id, status, data=None, error=None):
    if not properties or not properties.reply_to:
        logging.warning("Нет reply_to — ответ не отправлен")
        return

    response = {
        "correlation_id": correlation_id,
        "status": status,
        "data": serialize(data),
        "error": error
    }

    channel.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(response)
    )

def on_message(ch, method, properties, body):
    request = json.loads(body)
    request_id = request.get("id")
    action = request.get("action")
    data = request.get("data", {})
    version = request.get("version", "v1")

    # ---------- idempotency ----------
    cached = get_cached_response(request_id)
    if cached:
        send_response(
            properties,
            correlation_id=request_id,
            status=cached.get("status"),
            data=cached.get("data"),
            error=cached.get("error")
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # ---------- auth ----------
    if not check_api_key(request.get("auth")):
        send_response(properties, request_id, status="error", error="Unauthorized")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    db = next(get_db())

    try:
        response_data = None

        # ================= USERS =================
        if action == "user_get":
            service = UserService(db)
            user = service.get_user_by_id(data["user_id"])
            if not user:
                raise ValueError("User not found")
            response_data = (UserResponseV1 if version=="v1" else UserResponseV2).model_validate(user).model_dump()

        elif action == "user_list":
            service = UserService(db)
            page = data.get("page", 1)
            size = data.get("size", 10)
            users = service.get_users(page, size)
            if version == "v1":
                response_data = [(UserResponseV1).model_validate(u).model_dump() for u in users]
            else:
                response_data = {
                    "items": [UserResponseV2.model_validate(u).model_dump() for u in users],
                    "page": page,
                    "size": size
                }

        elif action == "user_create":
            service = UserService(db)
            user = service.create_user(UserCreate(**data))
            response_data = (UserResponseV1 if version=="v1" else UserResponseV2).model_validate(user).model_dump()

        elif action == "user_update":
            service = UserService(db)
            user = service.update_user(data["user_id"], UserUpdate(**data))
            response_data = (UserResponseV1 if version=="v1" else UserResponseV2).model_validate(user).model_dump()

        elif action == "user_delete":
            service = UserService(db)
            service.delete_user(data["user_id"])
            response_data = {"deleted_user_id": data["user_id"]}

        # ================= COURSES =================
        elif action == "course_get":
            service = CourseService(db)
            course = service.get_course_by_id(data["course_id"])
            if not course:
                raise ValueError("Course not found")
            response_data = (CourseResponseV1 if version=="v1" else CourseResponseV2).model_validate(course).model_dump()

        elif action == "course_list":
            service = CourseService(db)
            page = data.get("page", 1)
            size = data.get("size", 10)
            courses = service.get_all_courses(page, size)
            if version == "v1":
                response_data = [(CourseResponseV1).model_validate(c).model_dump() for c in courses]
            else:
                response_data = {
                    "items": [CourseResponseV2.model_validate(c).model_dump() for c in courses],
                    "page": page,
                    "size": size
                }

        elif action == "course_create":
            service = CourseService(db)
            course = service.create_course(CourseCreate(**data))
            response_data = (CourseResponseV1 if version=="v1" else CourseResponseV2).model_validate(course).model_dump()

        elif action == "course_update":
            service = CourseService(db)
            course = service.update_course(data["course_id"], CourseUpdate(**data))
            response_data = (CourseResponseV1 if version=="v1" else CourseResponseV2).model_validate(course).model_dump()

        elif action == "course_delete":
            service = CourseService(db)
            service.delete_course(data["course_id"])
            response_data = {"deleted_course_id": data["course_id"]}

        # ================= ENROLLMENTS =================
        elif action == "enrollment_get":
            service = EnrollmentService(db)
            enrollment = service.get_enrollment_by_id(data["enrollment_id"])
            if not enrollment:
                raise ValueError("Enrollment not found")
            response_data = (EnrollmentResponseV1 if version=="v1" else EnrollmentResponseV2).model_validate(enrollment).model_dump()

        elif action == "enrollment_list":
            service = EnrollmentService(db)
            page = data.get("page", 1)
            size = data.get("size", 10)
            enrollments = service.get_all_enrollments(page, size)
            if version == "v1":
                response_data = [(EnrollmentResponseV1).model_validate(e).model_dump() for e in enrollments]
            else:
                response_data = {
                    "items": [EnrollmentResponseV2.model_validate(e).model_dump() for e in enrollments],
                    "page": page,
                    "size": size
                }

        elif action == "enrollment_create":
            service = EnrollmentService(db)
            enrollment = service.create_enrollment(EnrollmentCreate(**data))
            response_data = (EnrollmentResponseV1 if version=="v1" else EnrollmentResponseV2).model_validate(enrollment).model_dump()

        elif action == "enrollment_delete":
            service = EnrollmentService(db)
            service.delete_enrollment(data["enrollment_id"])
            response_data = {"deleted_enrollment_id": data["enrollment_id"]}

        else:
            raise ValueError(f"Unknown action: {action}")

        safe_response = serialize(response_data)
        cache_response(request_id, safe_response)

        send_response(properties, request_id, status="ok", data=safe_response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Ошибка при обработке запроса {request_id}: {e}")
        # DLQ
        channel.basic_publish(exchange="", routing_key=DLQ_QUEUE, body=body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    finally:
        db.close()

# -------------------- START --------------------
channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_message)
logging.info(" [*] Unified worker (users, courses, enrollments) started")
channel.start_consuming()
