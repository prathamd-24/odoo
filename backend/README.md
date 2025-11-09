# Flask User Authentication API

A simple Flask application with SQLAlchemy for user authentication using session-based auth (no JWT tokens).

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Database Schema

The application uses SQLite with the following schema:

**Table: users**
- `id` - Integer (Primary Key)
- `email` - String (Unique, Required)
- `password_hash` - String (Required)
- `is_active` - Boolean (Default: True)
- `created_at` - DateTime

## API Endpoints

### 1. Register User
**POST** `/register`

**Request:**
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "mypassword123",
    "is_active": true
  }'
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true
  }
}
```

**Error Response (409):**
```json
{
  "error": "User already exists"
}
```

---

### 2. Login
**POST** `/login`

**Request:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "mypassword123"
  }'
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true
  }
}
```

**Error Response (401):**
```json
{
  "error": "Invalid email or password"
}
```

**Error Response (403):**
```json
{
  "error": "User account is not active"
}
```

**Note:** Use `-c cookies.txt` to save the session cookie and `-b cookies.txt` in subsequent requests to authenticate.

---

### 3. Get Profile (Protected)
**GET** `/profile`

**Request:**
```bash
curl -X GET http://localhost:5000/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2025-11-08T10:30:45.123456"
  }
}
```

**Error Response (401):**
```json
{
  "error": "Not authenticated"
}
```

---

### 4. Get All Users (Protected)
**GET** `/users`

**Request:**
```bash
curl -X GET http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "is_active": true,
      "created_at": "2025-11-08T10:30:45.123456"
    },
    {
      "id": 2,
      "email": "admin@example.com",
      "is_active": true,
      "created_at": "2025-11-08T11:15:22.789012"
    }
  ]
}
```

---

### 5. Update User (Protected)
**PUT** `/users/<user_id>`

**Request:**
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "email": "newemail@example.com",
    "password": "newpassword456",
    "is_active": false
  }'
```

**Response (200):**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "email": "newemail@example.com",
    "is_active": false
  }
}
```

**Note:** All fields are optional. You can update only the fields you need.

---

### 6. Delete User (Protected)
**DELETE** `/users/<user_id>`

**Request:**
```bash
curl -X DELETE http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "User deleted successfully"
}
```

---

### 7. Logout
**POST** `/logout`

**Request:**
```bash
curl -X POST http://localhost:5000/logout \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

---

## Complete Testing Flow

Here's a complete sequence of commands to test all endpoints:

```bash
# 1. Register first user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "password123"}'

# 2. Register second user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "bob@example.com", "password": "password456"}'

# 3. Login (save session cookie)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "alice@example.com", "password": "password123"}'

# 4. Get profile (using session cookie)
curl -X GET http://localhost:5000/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 5. Get all users
curl -X GET http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 6. Update user
curl -X PUT http://localhost:5000/users/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"is_active": false}'

# 7. Try to login with inactive user (should fail)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "bob@example.com", "password": "password456"}'

# 8. Delete user
curl -X DELETE http://localhost:5000/users/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 9. Logout
curl -X POST http://localhost:5000/logout \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 10. Try to access protected route without session (should fail)
curl -X GET http://localhost:5000/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

## Features

- ✅ User registration with email and password
- ✅ Session-based authentication (no JWT)
- ✅ Password hashing using werkzeug.security
- ✅ User activation status checking
- ✅ Protected routes requiring authentication
- ✅ CRUD operations for users
- ✅ SQLAlchemy ORM with SQLite database

## Notes

- The application uses session-based authentication with cookies
- Passwords are hashed using `werkzeug.security.generate_password_hash`
- The `is_active` field can be used to disable user accounts
- Protected routes check for session before allowing access
- Database file `users.db` will be created automatically in the project directory