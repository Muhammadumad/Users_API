# Users API (Task-01 & Task-02)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-DRF-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

REST API for user CRUD operations using Django REST Framework with persistent database storage (SQLite/MySQL).

## Features

- **Create, read, update, and delete users** with persistent storage
- **UUID-based user IDs** for unique identification
- **Persistent Database Storage** - SQLite (development) or MySQL (production)
- **Database Migrations** with Django ORM for schema versioning
- **Connection Pooling** for optimized database connections
- **Environment-based Configuration** using `.env` files
- **Validation** for email format and age constraints
- **Proper HTTP status codes** and error handling
- **Comprehensive test suite** with 7 passing tests
- **Postman collection** + testing guides included

## Task-02 Requirements Checklist

- ✅ CRUD endpoints for users with persistent database storage
- ✅ User fields: `id`, `name`, `email`, `age`, `created_at`, `updated_at`
- ✅ **Database Integration**: SQLite (dev) + MySQL (production)
- ✅ **ORM Integration**: Django ORM for model management
- ✅ **Database Migrations**: Schema versioning with Django migrations
- ✅ **Connection Pooling**: Connection timeout configuration
- ✅ **Environment Configuration**: `.env` file support with `python-dotenv`
- ✅ **Environment Variables**: Database credentials via `.env`
- ✅ `400` and `404` error handling with validation
- ✅ Email uniqueness enforced at database level

## Tech Stack

- **Python 3.14+**
- **Django 6.0.4**
- **Django REST Framework 3.17.1**
- **SQLite** (development default)
- **MySQL** (production-ready with mysqlclient)
- **mysqlclient 2.2.8** (MySQL adapter)
- **python-dotenv 1.0.0** (environment configuration)

## API Base URL

`http://localhost:8000`

## Endpoints

| Method   | Endpoint                     | Description                     | Success | Common Errors                        |
| -------- | ---------------------------- | ------------------------------- | ------- | ------------------------------------ |
| `POST`   | `/api/users/`                | Create user                     | `201`   | `400` invalid/missing/duplicate data |
| `GET`    | `/api/users/`                | List users                      | `200`   | -                                    |
| `GET`    | `/api/users/<uuid:user_id>/` | Get user by id                  | `200`   | `404` user not found                 |
| `PUT`    | `/api/users/<uuid:user_id>/` | Update user (partial supported) | `200`   | `400`, `404`                         |
| `DELETE` | `/api/users/<uuid:user_id>/` | Delete user                     | `204`   | `404` user not found                 |

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

## How the project works

This project is a small REST API built with Django and Django REST Framework to manage a `User` resource.

- Data model: `users.models.User` (fields: `id` UUID, `name`, `email` unique, `age`, `created_at`, `updated_at`).
- Storage: By default the project uses SQLite for local development. You can switch to MySQL by setting `DATABASE_HOST` and other database variables in `.env`.
- API layer: `users.views` exposes CRUD endpoints. Input/response validation is handled by DRF serializers (`users.serializers.UserSerializer`).
- Schema management: Django migrations are used to create and evolve the database schema.

Persistence behavior:

- In development (no `DATABASE_HOST` set) the project uses `db.sqlite3` (file). Data persists across server restarts.
- In production, configure MySQL via `.env` to persist data in a server-grade DB with connection pooling.

## Quick Start (SQLite - Development)

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Apply database migrations:

```powershell
python manage.py migrate
```

3. Run server:

```powershell
python manage.py runserver
```

4. Open:

- `http://localhost:8000/`
- `http://localhost:8000/api/users/`

## Database Setup

For production MySQL setup and detailed configuration, see [DATABASE_SETUP.md](DATABASE_SETUP.md).

### Switch to MySQL

Edit `.env`:

```env
DATABASE_HOST=localhost
DATABASE_NAME=users_api_db
DATABASE_USER=api_user
DATABASE_PASSWORD=your_password
```

Then run migrations:

```powershell
python manage.py migrate
```

## Developer notes / architecture summary

- `users/models.py` — Django ORM model representing users. Use `python manage.py makemigrations` and `python manage.py migrate` to update schema.
- `users/serializers.py` — DRF `ModelSerializer` mapping model fields to JSON and handling validation.
- `users/views.py` — Function-based API views for `user_list` and `user_detail` using ORM queries.
- `users/tests.py` — API test suite (7 tests) that runs against the configured database (uses test DB).
- `DATABASE_SETUP.md` — Step-by-step guide for switching to MySQL and production considerations.

## Recommended commands

Activate venv and install deps:

```powershell
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run migrations, tests, and start server:

```powershell
python manage.py migrate
python manage.py test users
python manage.py runserver
```

If you plan to use MySQL in production, ensure MySQL server is running and `.env` contains correct credentials before running `migrate`.

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
