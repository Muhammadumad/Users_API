# Postman Testing Guide - Users API

## Setup Instructions

Create a new Postman environment called `Users_API_Dev` with these variables:

```
base_url = http://localhost:8000
user_id = (set after creating a user)
```

## Endpoint 1: Create User

**Method:** `POST`

**URL:** `{{base_url}}/api/users/`

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

**Expected response:** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

**Post-request script:**

```javascript
const response = pm.response.json();
pm.environment.set("user_id", response.id);
```

## Endpoint 2: Get All Users

**Method:** `GET`

**URL:** `{{base_url}}/api/users/`

**Expected response:** `200 OK`

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "age": 28
  }
]
```

## Endpoint 3: Get User by ID

**Method:** `GET`

**URL:** `{{base_url}}/api/users/{{user_id}}/`

**Expected response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

## Endpoint 4: Update User

**Method:** `PUT`

**URL:** `{{base_url}}/api/users/{{user_id}}/`

**Headers:**

```
Content-Type: application/json
```

**Body:**

```json
{
  "name": "John Updated",
  "age": 29
}
```

**Expected response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Updated",
  "email": "john@example.com",
  "age": 29
}
```

## Endpoint 5: Delete User

**Method:** `DELETE`

**URL:** `{{base_url}}/api/users/{{user_id}}/`

**Expected response:** `204 No Content`

## Error Checks

Test these cases as part of the collection:

- Invalid email format returns `400 Bad Request`.
- Missing required fields return `400 Bad Request`.
- Unknown user ID returns `404 Not Found`.
- Reusing an existing email returns `400 Bad Request`.
