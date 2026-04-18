# Postman Tasks - Solutions Guide (Users CRUD)

## Prerequisites Setup

### Step 1: Start the Development Server

Run this command from the project folder:

```powershell
cd C:\Users\Muhammad Umad\users_api
python manage.py runserver
```

The API should be available at `http://localhost:8000`.

### Step 2: Import Postman Collection

1. Open Postman.
2. Click **Import**.
3. Select `Users_API_Postman_Collection.json`.
4. Import the collection.

### Step 3: Create Environment

Create a Postman environment named `Users_API_Dev` with:

```
base_url = http://localhost:8000
user_id =
```

Select this environment before sending requests.

## Task-by-Task Solutions

## Task 1: Create User

**Request**

- Method: `POST`
- URL: `{{base_url}}/api/users/`
- Headers: `Content-Type: application/json`
- Body:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

**Expected Response:** `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

**Postman test script**

```javascript
const response = pm.response.json();
pm.environment.set("user_id", response.id);
```

## Task 2: Get All Users

**Request**

- Method: `GET`
- URL: `{{base_url}}/api/users/`

**Expected Response:** `200 OK`

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

## Task 3: Get User by ID

**Request**

- Method: `GET`
- URL: `{{base_url}}/api/users/{{user_id}}/`

**Expected Response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

## Task 4: Update User

**Request**

- Method: `PUT`
- URL: `{{base_url}}/api/users/{{user_id}}/`
- Headers: `Content-Type: application/json`
- Body:

```json
{
  "name": "John Updated",
  "age": 29
}
```

**Expected Response:** `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Updated",
  "email": "john@example.com",
  "age": 29
}
```

## Task 5: Delete User

**Request**

- Method: `DELETE`
- URL: `{{base_url}}/api/users/{{user_id}}/`

**Expected Response:** `204 No Content`

## Error Handling Verification

Use these checks to confirm validation and status codes:

1. Invalid email format

- `POST /api/users/` with `"email": "not-an-email"`
- Expected: `400 Bad Request`

2. Missing required fields

- `POST /api/users/` without `name` or `age`
- Expected: `400 Bad Request`

3. Duplicate email

- Create same email twice
- Expected: `400 Bad Request`

4. User not found

- `GET /api/users/<random-uuid>/`
- Expected: `404 Not Found`

5. Empty update body

- `PUT /api/users/{{user_id}}/` with `{}`
- Expected: `400 Bad Request`

## Troubleshooting

1. `404 Not Found` on all requests

- Check route starts with `/api/users/`.
- Confirm `core/urls.py` includes `users.urls`.

2. `400 Bad Request` on create/update

- Ensure JSON is valid and fields match exactly: `name`, `email`, `age`.
- Ensure email uses valid format.
- Ensure age is a non-negative integer.

3. `user_id` variable is empty in Postman

- Run Task 1 again.
- Confirm the post-request script is present and environment is selected.

## Notes About In-Memory Storage

- Data is kept in a Python dictionary during runtime.
- Restarting the Django server clears all users.
- This behavior is expected for the assignment requirement.
