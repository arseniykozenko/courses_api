import json
import pika
from messaging.rabbitmq import channel
from messaging.queues import REQUEST_QUEUE, DLQ_QUEUE
from utils.auth import check_api_key
from utils.idempotency import get_cached_response, cache_response
from utils.database import get_db
from services.courses import CourseService
from services.users import UserService
from services.enrollments import EnrollmentService
from api.v2.schemas import CourseCreate, CourseUpdate, UserCreate, UserUpdate, EnrollmentCreate, CourseResponse, UserResponse, EnrollmentResponse

def send_response(properties, correlation_id, status, data=None, error=None):
    if not properties or not properties.reply_to:
        print("Нет reply_to, невозможно отправить ответ")
        return

    response = {
        "correlation_id": correlation_id,
        "status": status,
        "data": data,
        "error": error
    }

    channel.basic_publish(
        exchange='',
        routing_key=str(properties.reply_to),
        properties=pika.BasicProperties(
            correlation_id=str(properties.correlation_id)
        ),
        body=json.dumps(response)
    )

def on_message(ch, method, properties, body):
    request = json.loads(body)
    request_id = request.get("id")
    action = request.get("action")
    data = request.get("data", {})

    # Идемпотентность
    cached_response = get_cached_response(request_id)
    if cached_response:
        print(f"Идемпотентный ответ для {request_id}")
        send_response(properties, request_id, **cached_response)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Аутентификация
    if not check_api_key(request.get("auth")):
        send_response(properties, request_id, status="error", error="Unauthorized")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print("Авторизованный запрос:", request)

    db = get_db()

    try:
        response_data = {}

        # ----------------- USERS -----------------
        if action.startswith("user_"):
            service = UserService(db)
            if action == "user_get":
                user_id = data.get("user_id")
                user = service.get_user_by_id(user_id)
                if not user:
                    raise ValueError("Пользователь не найден")
                response_data = {
                    "status": "ok",
                    "data": UserResponse.model_validate(user).model_dump(),
                    "error": None
                }
            elif action == "user_create":
                user_obj = UserCreate(**data)
                new_user = service.create_user(user_obj)
                response_data = {
                    "status": "ok",
                    "data": UserResponse.model_validate(new_user).model_dump(),
                    "error": None
                }
            elif action == "user_update":
                user_id = data.get("user_id")
                user_obj = UserUpdate(**data)
                updated = service.update_user(user_id, user_obj)
                response_data = {
                    "status": "ok",
                    "data": UserResponse.model_validate(updated).model_dump(),
                    "error": None
                }
            elif action == "user_delete":
                user_id = data.get("user_id")
                user = service.get_user_by_id(user_id)
                if not user:
                    raise ValueError("Пользователь не найден")
                service.delete_user(user_id)
                response_data = {
                    "status": "ok",
                    "data": {"deleted_user_id": user_id},
                    "error": None
                }

        # ----------------- COURSES -----------------
        elif action.startswith("course_"):
            service = CourseService(db)
            if action == "course_get":
                course_id = data.get("course_id")
                course = service.get_course_by_id(course_id)
                if not course:
                    raise ValueError("Курс не найден")
                response_data = {
                    "status": "ok",
                    "data": CourseResponse.model_validate(course).model_dump(),
                    "error": None
                }
            elif action == "course_create":
                course_obj = CourseCreate(**data)
                new_course = service.create_course(course_obj)
                response_data = {
                    "status": "ok",
                    "data": CourseResponse.model_validate(new_course).model_dump(),
                    "error": None
                }
            elif action == "course_update":
                course_id = data.get("course_id")
                course_obj = CourseUpdate(**data)
                updated = service.update_course(course_id, course_obj)
                response_data = {
                    "status": "ok",
                    "data": CourseResponse.model_validate(updated).model_dump(),
                    "error": None
                }
            elif action == "course_delete":
                course_id = data.get("course_id")
                course = service.get_course_by_id(course_id)
                if not course:
                    raise ValueError("Курс не найден")
                service.delete_course(course_id)
                response_data = {
                    "status": "ok",
                    "data": {"deleted_course_id": course_id},
                    "error": None
                }

        # ----------------- ENROLLMENTS -----------------
        elif action.startswith("enrollment_"):
            service = EnrollmentService(db)
            user_service = UserService(db)
            course_service = CourseService(db)

            if action == "enrollment_create":
                enrollment_obj = EnrollmentCreate(**data)
                if not course_service.get_course_by_id(enrollment_obj.course_id):
                    raise ValueError("Курс не найден")
                if not user_service.get_user_by_id(enrollment_obj.user_id):
                    raise ValueError("Пользователь не найден")
                new_enrollment = service.create_enrollment(enrollment_obj)
                response_data = {
                    "status": "ok",
                    "data": EnrollmentResponse.model_validate(new_enrollment).model_dump(),
                    "error": None
                }
            elif action == "enrollment_delete":
                enrollment_id = data.get("enrollment_id")
                enrollment = service.get_enrollment_by_id(enrollment_id)
                if not enrollment:
                    raise ValueError("Запись на курс не найдена")
                service.delete_enrollment(enrollment_id)
                response_data = {
                    "status": "ok",
                    "data": {"deleted_enrollment_id": enrollment_id},
                    "error": None
                }
            elif action == "enrollment_get":
                enrollment_id = data.get("enrollment_id")
                enrollment = service.get_enrollment_by_id(enrollment_id)
                if not enrollment:
                    raise ValueError("Запись на курс не найдена")
                response_data = {
                    "status": "ok",
                    "data": EnrollmentResponse.model_validate(enrollment).model_dump(),
                    "error": None
                }
            elif action == "enrollment_get_by_user_id":
                user_id = data.get("user_id")
                enrollments = service.get_enrollments_by_user_id(user_id)
                response_data = {
                    "status": "ok",
                    "data": [EnrollmentResponse.model_validate(enrollment).model_dump() for enrollment in enrollments],
                    "error": None
                }
            elif action == "enrollment_get_by_course_id":
                course_id = data.get("course_id")
                enrollments = service.get_enrollments_by_course_id(course_id)
                response_data = {
                    "status": "ok",
                    "data": [EnrollmentResponse.model_validate(enrollment).model_dump() for enrollment in enrollments],
                    "error": None
                }

        else:
            raise ValueError(f"Неизвестное действие: {action}")

        # Кэшируем для идемпотентности
        cache_response(request_id, response_data)

        # Отправляем ответ клиенту
        send_response(properties, request_id, **response_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Ошибка при обработке {request_id}: {e}")
        # Отправка в DLQ
        channel.basic_publish(exchange='', routing_key=DLQ_QUEUE, body=body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Запуск worker
channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_message)
print(" [*] Worker для users, courses и enrollments запущен")
channel.start_consuming()
