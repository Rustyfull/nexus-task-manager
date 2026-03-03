# 🧪 API Testing Guide - Nexus Task Manager

## Quick Start Testing

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john_doe",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
  }'
```

**Response** (201 Created):
```json
{
  "user_id": 1,
  "email": "john@example.com",
  "username": "john_doe"
}
```

---

### 2. Login & Get Tokens
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save tokens for next requests:**
```bash
export ACCESS_TOKEN="<your_access_token>"
export REFRESH_TOKEN="<your_refresh_token>"
```

---

### 3. Get Current User Info
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-02-27T10:30:00",
  "updated_at": "2024-02-27T10:30:00"
}
```

---

### 4. Create a Project
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete redesign of company website"
  }'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "Website Redesign",
  "description": "Complete redesign of company website",
  "status": "planning",
  "owner_id": 1,
  "created_at": "2024-02-27T10:32:00",
  "updated_at": "2024-02-27T10:32:00"
}
```

**Save project ID:**
```bash
export PROJECT_ID=1
```

---

### 5. List Your Projects
```bash
curl -X GET http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (200 OK):
```json
{
  "total": 1,
  "skip": 0,
  "limit": 100,
  "items": [
    {
      "id": 1,
      "name": "Website Redesign",
      "description": "Complete redesign of company website",
      "status": "planning",
      "owner_id": 1,
      "created_at": "2024-02-27T10:32:00",
      "updated_at": "2024-02-27T10:32:00"
    }
  ]
}
```

---

### 6. Create a Task
```bash
curl -X POST http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design homepage mockup",
    "description": "Create responsive mockup for homepage",
    "priority": "high",
    "due_date": "2024-03-15T00:00:00"
  }'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Design homepage mockup",
  "description": "Create responsive mockup for homepage",
  "status": "open",
  "priority": "high",
  "project_id": 1,
  "assignee_id": null,
  "due_date": "2024-03-15T00:00:00",
  "created_at": "2024-02-27T10:35:00",
  "updated_at": "2024-02-27T10:35:00"
}
```

**Save task ID:**
```bash
export TASK_ID=1
```

---

### 7. List Project Tasks
```bash
curl -X GET http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (200 OK):
```json
{
  "total": 1,
  "skip": 0,
  "limit": 100,
  "items": [
    {
      "id": 1,
      "title": "Design homepage mockup",
      "description": "Create responsive mockup for homepage",
      "status": "open",
      "priority": "high",
      "project_id": 1,
      "assignee_id": null,
      "due_date": "2024-03-15T00:00:00",
      "created_at": "2024-02-27T10:35:00",
      "updated_at": "2024-02-27T10:35:00"
    }
  ]
}
```

---

### 8. Update Task Status
```bash
curl -X PUT http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks/$TASK_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": "critical"
  }'
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Design homepage mockup",
  "description": "Create responsive mockup for homepage",
  "status": "in_progress",
  "priority": "critical",
  "project_id": 1,
  "assignee_id": null,
  "due_date": "2024-03-15T00:00:00",
  "created_at": "2024-02-27T10:35:00",
  "updated_at": "2024-02-27T10:40:00"
}
```

---

### 9. Assign Task to User
```bash
curl -X PUT http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks/$TASK_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assignee_id": 1,
    "status": "in_progress"
  }'
```

---

### 10. Update Project Status
```bash
curl -X PUT http://localhost:8000/api/v1/projects/$PROJECT_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active"
  }'
```

---

### 11. Delete Task
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks/$TASK_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (204 No Content): Empty response

---

### 12. Delete Project
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/$PROJECT_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (204 No Content): Empty response

---

## Error Scenarios

### Invalid Token
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer invalid_token"
```

**Response** (401 Unauthorized):
```json
{
  "detail": "Token expired"
}
```

---

### Insufficient Permissions
```bash
# Create second user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "username": "jane_doe",
    "password": "SecurePassword123!"
  }'

# Login as Jane
export JANE_TOKEN="<jane's_access_token>"

# Try to delete John's project (should fail)
curl -X DELETE http://localhost:8000/api/v1/projects/1 \
  -H "Authorization: Bearer $JANE_TOKEN"
```

**Response** (403 Forbidden):
```json
{
  "detail": "Not authorized to delete this project"
}
```

---

### Not Found
```bash
curl -X GET http://localhost:8000/api/v1/projects/999 \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Response** (404 Not Found):
```json
{
  "detail": "Project not found"
}
```

---

## Postman Collection

Import this as a Postman collection for easier testing:

```json
{
  "info": {
    "name": "Nexus Task Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/v1/auth/register",
            "body": {
              "raw": "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"SecurePass123!\"}"
            }
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/v1/auth/login",
            "body": {
              "raw": "{\"email\":\"test@example.com\",\"password\":\"SecurePass123!\"}"
            }
          }
        }
      ]
    },
    {
      "name": "Projects",
      "item": [
        {
          "name": "Create Project",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/v1/projects",
            "header": {
              "Authorization": "Bearer {{access_token}}"
            },
            "body": {
              "raw": "{\"name\":\"Test Project\"}"
            }
          }
        }
      ]
    }
  ]
}
```

---

## Testing with Swagger UI

1. Open browser: `http://localhost:8000/api/v1/docs`
2. Click "Try it out" on any endpoint
3. Enter parameters
4. Click "Execute"
5. See live response

---

## Authentication Workflow (Diagram)

```
1. Register
   ├─→ POST /auth/register
   └─→ Get user_id

2. Login
   ├─→ POST /auth/login
   └─→ Get access_token & refresh_token

3. Use Token
   ├─→ Add header: Authorization: Bearer <access_token>
   └─→ Make authenticated requests

4. Token Expires
   ├─→ POST /auth/refresh with refresh_token
   └─→ Get new access_token

5. Continue using new token
```

---

## Common Testing Patterns

### Pagination
```bash
# Get first page
curl "http://localhost:8000/api/v1/projects?skip=0&limit=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Get second page
curl "http://localhost:8000/api/v1/projects?skip=10&limit=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Filtering Tasks by Status
```bash
curl "http://localhost:8000/api/v1/projects/$PROJECT_ID/tasks?status=in_progress" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Full Workflow Test
```bash
#!/bin/bash
set -e

BASE_URL="http://localhost:8000"

# 1. Register
REGISTER=$(curl -s -X POST $BASE_URL/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Pass123!"}')

# 2. Login
LOGIN=$(curl -s -X POST $BASE_URL/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123!"}')
TOKEN=$(echo $LOGIN | jq -r '.access_token')

# 3. Create project
PROJECT=$(curl -s -X POST $BASE_URL/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Project"}')
PROJECT_ID=$(echo $PROJECT | jq -r '.id')

# 4. Create task
TASK=$(curl -s -X POST $BASE_URL/api/v1/projects/$PROJECT_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task"}')

echo "✅ Full workflow test passed!"
```

---

Viel Spaß beim Testen! 🚀
