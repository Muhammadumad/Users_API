# Task-01: Basic REST API with CRUD Operations

This project implements a basic REST API for a users resource using Django REST Framework.

## Assignment Coverage

The API satisfies the Task-01 requirements:

- CRUD endpoints for users
- User fields: `id` (UUID), `name`, `email`, `age`
- In-memory storage using a hashmap-style Python dictionary
- Proper status codes and error handling (`200`, `201`, `204`, `400`, `404`)
- Basic input validation (including valid email format)

## Tech Stack

- Python
- Django
- Django REST Framework

## Project Structure

- `users/views.py`: CRUD endpoint logic
- `users/serializers.py`: input validation and UUID generation
- `users/store.py`: in-memory `USERS` dictionary and email helpers
- `users/urls.py`: users API routes
- `core/urls.py`: root and API routing
- `users/tests.py`: API test cases
- `Users_API_Postman_Collection.json`: ready Postman collection

## API Base URL

`http://localhost:8000`

## Endpoints

### 1) Create User

- Method: `POST`
- URL: `/api/users/`
- Request body:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

- Success response: `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

### 2) Get All Users

- Method: `GET`
- URL: `/api/users/`
- Success response: `200 OK`

### 3) Get User By ID

- Method: `GET`
- URL: `/api/users/<uuid:user_id>/`
- Success response: `200 OK`
- Not found response: `404 Not Found`

### 4) Update User

- Method: `PUT`
- URL: `/api/users/<uuid:user_id>/`
- Request body (partial updates supported):

```json
{
  "name": "John Updated",
  "age": 29
}
```

- Success response: `200 OK`
- Invalid payload response: `400 Bad Request`
- Not found response: `404 Not Found`

### 5) Delete User

- Method: `DELETE`
- URL: `/api/users/<uuid:user_id>/`
- Success response: `204 No Content`
- Not found response: `404 Not Found`

## Validation Rules

- `name`: required, max 100 characters
- `email`: required, must be valid email format
- `age`: required, integer, minimum `0`
- Duplicate email is rejected with `400 Bad Request`

## Error Handling

- `400 Bad Request`
  - invalid email
  - missing required fields
  - duplicate email
  - empty update body
- `404 Not Found`
  - user UUID does not exist

## In-Memory Storage Note

User data is stored in-memory in `users/store.py` (`USERS` dictionary).

This means all users are cleared when the Django server restarts.

## Local Setup and Run

1. Create and activate virtual environment (if not already active)
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run server:

```powershell
python manage.py runserver
```

4. Open:

- API root: `http://localhost:8000/`
- Users list/create: `http://localhost:8000/api/users/`

## Run Tests

```powershell
python manage.py test users
```

## Postman Testing

Use the included collection:

- `Users_API_Postman_Collection.json`

Environment variables:

- `base_url = http://localhost:8000`
- `user_id = ` (auto-set after Create User)

Supporting docs:

- `POSTMAN_TESTING_GUIDE.md`
- `POSTMAN_SOLUTIONS.md`

## Sample cURL

Create user:

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":28}'
```

Get user by id:

```bash
curl http://localhost:8000/api/users/<USER_UUID>/
```
