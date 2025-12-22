# Courses API - Messaging Worker

## Introduction
CourseAPI — это сервис для управления пользователями, курсами и записями на курсы.
В этой лабораторной используется RabbitMQ для обмена сообщениями вместо REST API.
Клиент публикует запросы в очередь api.requests, worker обрабатывает их и отправляет ответ в очередь api.responses.

## Installation
Выполните следующие действия, чтобы установить и запустить приложение.

1. Склонируйте репозиторий
   ```
   git clone https://github.com/username/courses_api.git
   ```
3. Перейдите в директорию проекта
    ```
    cd courses_api
    ```
4. Создайте файл окружения .env. Пример:
    ```
    DATABASE_URL=postgresql://postgres:admin@db:5432/courses_db
    RABBITMQ_HOST=rabbitmq
    RABBITMQ_USER=admin
    RABBITMQ_PASS=admin
    RABBITMQ_PORT=5672
    INTERNAL_API_KEY=example-key

    ```
5. Запустите все необходимые сервисы с помощью docker-compose
    ```
    docker-compose up --build
    ```
6. Запустите тест-клиент
    ```
    python -m messaging.client_test
    ```
## Архитектура
#### Queues:
```
api.requests — входящие запросы.
api.responses — исходящие ответы.
dlq.requests — Dead Letter Queue для необрабатываемых сообщений.
```
#### Properties:
```
correlation_id — уникальный идентификатор запроса.
reply_to — очередь, куда worker отправляет ответ.
```
#### Versioning: 
поддерживаются версии сообщений (v1, v2). В v2 добавлены пагинация (page, size) и новые схемы response.

## Аутентификация:
  Для всех запросов требуется auth ключ (API key), передаваемый в поле auth сообщения.
  Если ключ неверный → возвращается статус error и сообщение "Unauthorized".
  Idempotency ключ (request ID / correlation_id) защищает от дублирующих запросов.
## Примеры запросов и ответов
Примеры запросов описаны ниже.
### [1] User Create
#### Request
```
{
  "id": "uuid-1234",
  "version": "v2",
  "action": "user_create",
  "data": {
    "email": "student@example.com",
    "first_name": "Alexey",
    "last_name": "Petrov",
    "patronymic": "Ivanovich",
    "password": "123456"
  },
  "auth": "api-key"
}
```
#### Response
```
{
  "correlation_id": "uuid-1234",
  "status": "ok",
  "data": {
    "id": 1,
    "email": "student@example.com",
    "first_name": "Alexey",
    "last_name": "Petrov",
    "patronymic": "Ivanovich",
    "created_at": <ISO_TIMESTAMP>,
    "updated_at": <ISO_TIMESTAMP>
  },
  "error": null
}

```

### [2] Get Courses
#### Request
```
{
  "id": "uuid-5678",
  "version": "v2",
  "action": "course_list",
  "data": {
    "page": 1,
    "size": 10
  },
  "auth": "api-key"
}

```
#### Response
```
{
  "correlation_id": "uuid-5678",
  "status": "ok",
  "data": {
    "items": [
      {"id": 1, "title": "Математика", "description": "Курс по математике"},
      {"id": 2, "title": "Программирование", "description": "Программирование на Python"}
    ],
    "page": 1,
    "size": 10
  },
  "error": null
}

```

### [3] Ошибка авторизации (Unauthorized)
#### Response
```
{
  "correlation_id": "uuid-5678",
  "status": "error",
  "data": null,
  "error": "Unauthorized"
}
```

### [4] Повторный запрос (Idempotency)
```
Если id запроса уже обработан, worker возвращает кешированный ответ.
Дублирующие операции не выполняются, данные не изменяются.
```

### [5] Dead Letter Queue (DLQ)
#### Request
```
Сообщения, вызвавшие необрабатываемые ошибки (например, Unknown action), отправляются в очередь dlq.requests.
Позволяет анализировать и повторно обрабатывать проблемные сообщения.
```

### Тестирование
Для тестирования есть messaging/client_test.py, который отправляет запросы и получает ответы через RabbitMQ.
Пример вызова:
#### Request
```
response = send_request("user_create", {
    "email": "student@example.com",
    "first_name": "Alexey",
    "last_name": "Petrov",
    "patronymic": "Ivanovich",
    "password": "123456"
})
print(response)
```