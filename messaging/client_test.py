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


# ---------------- USERS ----------------

def test_users():
    print("\n=== USERS ===")

    # create
    resp = send_request("user_create", {
        "email": "student@example.com",
        "first_name": "Alexey",
        "last_name": "Petrov",
        "patronymic": "Ivanovich",
        "password": "123456",
    }, request_id="user_create")
    user_id = resp["data"]["id"]
    print("User created:", resp)

    # get
    resp = send_request("user_get", {"user_id": user_id})
    print("User get:", resp)

    # list
    resp = send_request("user_list", {"page": 1, "size": 10})
    print("User list:", resp)

    # update
    resp = send_request("user_update", {
        "user_id": user_id,
        "first_name": "Nikita",
        "last_name": "Ivanov",
        "patronymic": "Petrovich"
    })
    print("User updated:", resp)

    # delete
    resp = send_request("user_delete", {"user_id": user_id})
    print("User deleted:", resp)

# ---------------- COURSES ----------------

def test_courses():
    print("\n=== COURSES ===")

    # create
    resp = send_request("course_create", {
        "title": "RabbitMQ Course",
        "description": "Async API"
    }, request_id="course_create")
    course_id = resp["data"]["id"]
    print("Course created:", resp)

    resp = send_request("course_get", {"course_id": course_id})
    print("Course get:", resp)

    # list
    resp = send_request("course_list", {"page": 1, "size": 10})
    print("Course list:", resp)

    # update
    resp = send_request("course_update", {
        "course_id": course_id,
        "title": "Updated Course"
    })
    print("Course updated:", resp)

    # delete
    resp = send_request("course_delete", {"course_id": course_id})
    print("Course deleted:", resp)

# ---------------- ENROLLMENTS ----------------

def test_idempotency():
    print("\n=== IDEMPOTENCY ===")

    # resp = send_request("user_delete", {"user_id": 6})
    # print("User deleted:", resp)

    # create user
    resp = send_request("user_create", {
        "email": "student@example.com",
        "first_name": "Alexey",
        "last_name": "Petrov",
        "patronymic": "Ivanovich",
        "password": "123456",
    }, request_id="user_create")
    print("User created:", resp)

def test_enrollments():
    print("\n=== ENROLLMENTS ===")

    # create user
    user = send_request("user_create", {
        "email": "student@example.com",
        "first_name": "Alexey",
        "last_name": "Petrov",
        "patronymic": "Ivanovich",
        "password": "123456",
    }, request_id="user_create")["data"]

    # create course
    course = send_request("course_create", {
        "title": "Python Async",
        "description": "RabbitMQ"
    }, request_id="course_create")["data"]

    # create enrollment
    resp = send_request("enrollment_create", {
        "user_id": user["id"],
        "course_id": course["id"]
    }, request_id="enrollment_create")
    enrollment_id = resp["data"]["id"]
    print("Enrollment created:", resp)

    # get
    resp = send_request("enrollment_get", {"enrollment_id": enrollment_id})
    print("Enrollment get:", resp)

    # list
    resp = send_request("enrollment_list", {"page": 1, "size": 10})
    print("Enrollment list:", resp)

    # delete
    resp = send_request("enrollment_delete", {"enrollment_id": enrollment_id})
    print("Enrollment deleted:", resp)

    # cleanup
    send_request("user_delete", {"user_id": user["id"]})
    send_request("course_delete", {"course_id": course["id"]})

# ---------------- MAIN ----------------

if __name__ == "__main__":
    test_idempotency()
    # test_users()
    test_courses()
    # test_enrollments()

    print("\n✅ ALL TESTS PASSED")