# Users API (Task-01)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-DRF-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Basic REST API for user CRUD operations using Django REST Framework with in-memory storage.

## Features

- Create, read, update, and delete users
- UUID-based user IDs
- In-memory hashmap-style storage (Python dictionary)
- Validation for email and age
- Proper HTTP status codes and error handling
- Postman collection + testing guide included

## Assignment Checklist

- CRUD endpoints for users
- User fields: `id`, `name`, `email`, `age`
- In-memory store (no DB persistence for users CRUD flow)
- `400` and `404` handling
- Email format validation

## Tech Stack

- Python
- Django
- Django REST Framework

## API Base URL

`http://localhost:8000`

## Endpoints

| Method | Endpoint | Description | Success | Common Errors |
|---|---|---|---|---|
| `POST` | `/api/users/` | Create user | `201` | `400` invalid/missing/duplicate data |
| `GET` | `/api/users/` | List users | `200` | - |
| `GET` | `/api/users/<uuid:user_id>/` | Get user by id | `200` | `404` user not found |
| `PUT` | `/api/users/<uuid:user_id>/` | Update user (partial supported) | `200` | `400`, `404` |
| `DELETE` | `/api/users/<uuid:user_id>/` | Delete user | `204` | `404` user not found |

## Sample Request and Response

### Create User

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

## Validation Rules

- `name`: required, max 100 chars
- `email`: required, valid email format
- `age`: required, integer, minimum `0`
- duplicate email rejected

## Important Note: In-Memory Storage

Users are stored in `users/store.py` in the `USERS` dictionary.

When the server restarts, stored users are cleared. This is expected for this assignment.

## Quick Start

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Run server:

```powershell
python manage.py runserver
```

3. Open:

- `http://localhost:8000/`
- `http://localhost:8000/api/users/`

## Run Tests

```powershell
python manage.py test users
```

## Postman

- Collection: `Users_API_Postman_Collection.json`
- Environment variables:
  - `base_url = http://localhost:8000`
  - `user_id =` (auto-set after create)
- Guides:
  - `POSTMAN_TESTING_GUIDE.md`
  - `POSTMAN_SOLUTIONS.md`

## cURL Examples

Create user:

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":28}'
```

Get user by ID:

```bash
curl http://localhost:8000/api/users/<USER_UUID>/
```

## License

This project is licensed under the MIT License. See `LICENSE`.
