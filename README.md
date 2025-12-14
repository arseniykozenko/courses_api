# Courses API

## Introduction
CourseAPI — это сервис для управления пользователями, курсами и записями на курсы.
Система предоставляет операции для регистрации пользователей, аутентификации, получения списка пользователей, создания курсов и записей на курсы.

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
    INTERNAL_API_KEY=example-key
    ```
5. Запустите все необходимые сервисы с помощью docker-compose
    ```
    docker-compose up --build
    ```
6. Перейдите в документацию Swagger UI
    ```
    http://localhost:8080/docs
    ```
## Аутентификация
В API используется JWT Bearer Authentication.
После успешного логина необходимо передавать токен в заголовке с помощью Authorize:
    ```
    Authorization: Bearer <ACCESS_TOKEN>
    ```
## REST API
Примеры запросов описаны ниже.
### [1] Register
#### Request
`POST /api/v2/auth/register`
```
curl -X POST \
  'http://localhost:8080/api/v2/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@gmail.com",
    "password": "testpass",
    "first_name": "Ivanov",
    "last_name": "Ivan",
    "patronymic": "Ivanovich"
  }'
```
#### Response
```
{
    "id": <USER_ID>
    "email": "test@gmail.com",
    "password": "testpass",
    "first_name": "Ivanov",
    "last_name": "Ivan",
    "patronymic": "Ivanovich"
    "created_at": <ISO_TIMESTAMP>
    "updatet_at": <ISO_TIMESTAMP>
}
```

### [2] Login
#### Request
`POST /api/v2/auth/login`
```
curl -X POST \
  'http://localhost:8080/api/v2/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@gmail.com",
    "password": "testpass"
  }'
```
#### Response body
```
{
  "access": "<YOUR_ACCESS_TOKEN>"
  "token_type: "Bearer"
}
```

### [3] Get list of Courses
#### Request
`GET /api/v2/courses/`
```
curl -X GET \
  'http://localhost:8080/api/v2/courses/?page=1&size=10&fields=id,title' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```
#### Response body
```
[
  {
    "id": <COURSE_ID>,
    "title": "Математика",
  },
  {
    "id": <COURSE_ID>,
    "title": "Программирование",
  },
]
```

### [4] Create course
#### Request
`POST /api/v2/courses/`
```
curl -X POST \
  'http://localhost:8080/api/v2/courses/' \
  -H 'accept: application/json' \
  -H 'IdempotencyKey: course123' \
  -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Английский Язык",
    "description": "Уроки английского языка"
  }'
```
#### Response body
```
{
  "id": <COURSE_ID>,
  "title": "Английский язык",
  "description": "Уроки английского языка",
  "created_at": <ISO_TIMESTAMP>,
  "updated_at": <ISO_TIMESTAMP>
}
```

### [5] Get course by ID
#### Request
`GET /api/v2/courses/{id}`
```
curl -X GET \
  'http://localhost:8080/api/v2/courses/<COURSE_ID>?fields=id,title,description' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_ACCESS_TOKEN>'
```
#### Response body
```
{
  "id": <COURSE_ID>,
  "title": "Математика",
  "description": "Основы математики",
}
```
### [6] Ограничение частоты запросов (Rate Limiting)
```
Все конечные точки API защищены ограничением частоты запросов.
При превышении лимита сервер возвращает ответ:
```
#### Response body
```
```
{
  "detail": "Too many requests"
}
```
```
#### Response headers
```
retry-after: 60
x-limit-remaining: 0
```