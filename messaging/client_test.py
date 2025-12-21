import json
import uuid
import pika
from messaging.rabbitmq import channel
from messaging.queues import REQUEST_QUEUE

def send_request(action, data, request_id=None):
    """Отправка запроса в RabbitMQ и ожидание ответа"""
    correlation_id = request_id or str(uuid.uuid4())
    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    response = {}

    def on_response(ch, method, properties, body):
        resp = json.loads(body)
        if properties.correlation_id == correlation_id:
            response.update(resp)
            ch.stop_consuming()

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    request = {
        "id": correlation_id,
        "version": "v2",
        "action": action,
        "data": data,
        "auth": "API_KEY_123"
    }

    channel.basic_publish(
        exchange='',
        routing_key=REQUEST_QUEUE,
        body=json.dumps(request),
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=correlation_id
        )
    )

    print(f"Запрос отправлен: {action} (id={correlation_id})")
    channel.start_consuming()
    return response


print("\n=== TEST USERS ===")
user_data = {"email": "test1@example.com", "name": "Test User"}
user_resp = send_request("user_create", user_data)
print("Создан пользователь:", user_resp)

user_resp2 = send_request("user_create", user_data, request_id=user_resp["correlation_id"])
print("Повторный идемпотентный запрос:", user_resp2)

get_user_resp = send_request("user_get", {"user_id": user_resp["data"]["id"]})
print("Получение пользователя:", get_user_resp)


print("\n=== TEST COURSES ===")
course_data = {"title": "Python 101", "description": "Intro"}
course_resp = send_request("course_create", course_data)
print("Создан курс:", course_resp)

get_course_resp = send_request("course_get", {"course_id": course_resp["data"]["id"]})
print("Получение курса:", get_course_resp)


print("\n=== TEST ENROLLMENTS ===")
enroll_data = {"user_id": user_resp["data"]["id"], "course_id": course_resp["data"]["id"]}
enroll_resp = send_request("enrollment_create", enroll_data)
print("Создана запись на курс:", enroll_resp)

get_enroll_resp = send_request("enrollment_get", {"enrollment_id": enroll_resp["data"]["id"]})
print("Получение записи на курс:", get_enroll_resp)


print("\n=== TEST DLQ / TEMP ERROR ===")
temp_error_resp = send_request("crash_temp", {"user_id": 1})
print("Реакция на временную ошибку:", temp_error_resp)