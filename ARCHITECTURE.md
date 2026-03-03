# 🏗️ Nexus Task Manager - Architecture Document

## Overview

Nexus Task Manager follows **Hexagonal Architecture** (Ports & Adapters) with a layered design that ensures clean separation of concerns, testability, and maintainability.

---

## Architecture Layers

### 1. **Presentation Layer (API)**
- **Location**: `app/api/v1/`
- **Responsibility**: HTTP endpoint handling
- **Components**:
  - Route handlers (auth, users, projects, tasks)
  - Request/response serialization
  - HTTP status code management
  - Dependency injection

**Example Flow**:
```
HTTP Request → FastAPI Route → Dependency Resolution → Service Call → Response
```

### 2. **Business Logic Layer (Services)**
- **Location**: `app/services/`
- **Responsibility**: Core business rules and workflows
- **Components**:
  - `AuthService`: Login, registration, token management
  - `UserService`: User profile management
  - `ProjectService`: Project CRUD with authorization
  - `TaskService`: Task management with RBAC

**Key Features**:
- Authorization checks
- Business rule validation
- Cross-entity operations
- Error handling

### 3. **Data Access Layer (Repository)**
- **Location**: `app/repository/`
- **Responsibility**: Database interactions abstraction
- **Components**:
  - `UserRepository`: User queries and mutations
  - `ProjectRepository`: Project data operations
  - `TaskRepository`: Task data operations

**Benefits**:
- Abstraction from SQLAlchemy details
- Testability via mocking
- Query optimization in one place
- Complex query logic encapsulation

### 4. **Domain Layer (Models)**
- **Location**: `app/models/`
- **Responsibility**: Data structure definitions
- **Components**:
  - Base models with timestamps
  - SQLAlchemy ORM models
  - Database relationships
  - Constraints and indexes

### 5. **Cross-Cutting Concerns**
- **Location**: `app/core/`
- **Components**:
  - `config.py`: Configuration management (Pydantic Settings)
  - `security.py`: JWT and password utilities
  - `database.py`: Async database setup
  - `constants.py`: Enums and constants

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     HTTP Request                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              API Router Layer (v1/auth.py)                    │
│  - Parse request                                              │
│  - Validate input with Pydantic                              │
│  - Dependency injection (get_session, current_user)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Service Layer (services/auth_service.py)            │
│  - Business logic (authentication)                            │
│  - Authorization checks                                       │
│  - Token generation                                           │
│  - Error handling                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        Repository Layer (repository/user_repository.py)       │
│  - Database queries (SELECT)                                  │
│  - Data mutations (INSERT, UPDATE, DELETE)                   │
│  - Query optimization                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│     Database Layer (models/ + SQLAlchemy)                     │
│  - ORM mapping                                                │
│  - SQL execution                                              │
│  - Transaction management                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                              │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              HTTP Response (JSON)                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependency Injection Pattern

### Current Implementation

```python
# API layer requests dependencies
@router.post("/login")
async def login(
    credentials: TokenRequest,
    session: AsyncSession = Depends(get_session)
):
    # Session is injected by FastAPI
    service = AuthService(session)
    result = await service.authenticate_user(...)
    return result
```

### Dependency Chain
```
FastAPI Route
    ↓
get_session (provides AsyncSession)
    ↓
AuthService(session)
    ↓
UserRepository(session)
    ↓
SQLAlchemy ORM queries
    ↓
PostgreSQL
```

---

## Authorization & RBAC Flow

### Middleware Chain

```
1. HTTP Request with Bearer Token
        ↓
2. HTTPBearer extracts token from Authorization header
        ↓
3. get_current_user dependency validates token
        ↓
4. JWT decoded and user loaded from database
        ↓
5. Endpoint receives authenticated User object
        ↓
6. Service layer checks user.role against required roles
        ↓
7. HTTPException(403) if unauthorized
        ↓
8. Business logic proceeds
```

### Role Hierarchy
```
ADMIN
  ↓ (can do everything)
  ├─→ Delete any project
  ├─→ Delete any task
  ├─→ Deactivate any user
  ├─→ View all projects
  └─→ Approve all operations

MANAGER
  ├─→ Create projects
  ├─→ Assign tasks
  └─→ View team tasks

USER
  ├─→ Create their own projects
  ├─→ Update assigned tasks
  └─→ View own data
```

---

## Async/Await Architecture

### Why Async?

- **Non-blocking I/O**: Multiple database queries in parallel
- **Scalability**: Handle 10,000+ concurrent connections
- **Performance**: Minimal thread overhead

### Async Pattern

```python
# Every service and repository method is async
class UserRepository:
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)  # Non-blocking
        return result.scalar_one_or_none()

# Services are async
class AuthService:
    async def authenticate_user(self, email: str, password: str) -> dict | None:
        user = await self.repo.get_by_email(email)  # Awaits async call
        if user and security_service.verify_password(password, user.hashed_password):
            return {"access_token": ...}
```

---

## Testing Strategy

### Test Pyramid

```
         /\
        /  \    End-to-End Tests (5%)
       /    \   - Full API workflows
      /──────\  - Database integration
     /        \
    /          \
   /            \
  /──────────────\  Integration Tests (25%)
 /                \ - API endpoints with DB
/__________________ \ - Authorization flows

   Unit Tests (70%)
   - Service logic
   - Repository queries
   - Security functions
```

### Test Organization

```
tests/
├── conftest.py           # Fixtures & setup
├── test_auth.py          # Auth endpoint tests
├── test_users.py         # User endpoint tests
├── test_projects.py      # Project endpoint tests
├── test_tasks.py         # Task endpoint tests
├── test_health.py        # Health endpoint tests
└── test_security.py      # Security unit tests
```

### Coverage Goals
- **Target**: >80% line coverage
- **Critical**: 100% for security.py, auth services
- **Focus**: Authorization and business logic

---

## Database Design

### Entity-Relationship Diagram

```
┌──────────────┐
│    User      │
├──────────────┤
│ id (PK)      │
│ email (UK)   │
│ username (UK)│
│ password     │
│ role         │
│ is_active    │
└──────────────┘
    │
    │ owns (1-N)
    │
    ├─→ ┌──────────────────┐
    │   │     Project      │
    │   ├──────────────────┤
    │   │ id (PK)          │
    │   │ name             │
    │   │ description      │
    │   │ owner_id (FK)    │
    │   │ status           │
    │   └──────────────────┘
    │       │
    │       │ contains (1-N)
    │       │
    │       └─→ ┌──────────────────┐
    │           │      Task        │
    │           ├──────────────────┤
    │           │ id (PK)          │
    │           │ title            │
    │           │ project_id (FK)  │
    │           │ assignee_id (FK) │
    │           │ status           │
    │           │ priority         │
    │           └──────────────────┘
    │
    └─→ ┌──────────────────────┐
        │   ProjectMember      │
        ├──────────────────────┤
        │ id (PK)              │
        │ project_id (FK)      │
        │ user_id (FK)         │
        │ role                 │
        └──────────────────────┘
```

### Key Design Decisions

1. **Timestamps on All Models**: `created_at`, `updated_at` for audit trail
2. **Soft Deletes**: `is_active` flag for users instead of hard delete
3. **Cascading Deletes**: Projects/tasks deleted when owner deleted
4. **Unique Constraints**: Email, username at database level
5. **Indexes**: On frequently queried columns (owner_id, project_id, assignee_id)

---

## Security Architecture

### Authentication Flow

```
User Input (email, password)
    ↓
Validate with Pydantic
    ↓
Query user by email
    ↓
Compare passwords with bcrypt.verify()
    ↓
If valid:
  - Generate JWT access token (30 min)
  - Generate JWT refresh token (7 days)
  - Return both tokens
    ↓
Response: {"access_token": "...", "refresh_token": "..."}
```

### JWT Token Structure

```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "123",           # User ID
  "email": "user@...",    # User email
  "role": "admin",        # User role
  "exp": 1234567890,      # Expiration
  "type": "access"        # Token type
}

Signature: HMACSHA256(header.payload, SECRET_KEY)
```

### Authorization Checks

```
@router.put("/api/v1/projects/{project_id}")
async def update_project(
    project_id: int,
    current_user = Depends(get_current_user)  # Validates JWT
):
    # Service checks authorization
    if project.owner_id != current_user.id and current_user.role != ADMIN:
        raise PermissionError()
    
    # Only proceed if authorized
    return update_project(...)
```

---

## Performance Optimizations

### 1. Database Query Optimization
- **Indexes** on frequently queried columns
- **Join queries** to avoid N+1 problems
- **Limit results** with pagination

### 2. Async I/O
- Non-blocking database calls
- Concurrent request handling
- Connection pooling (20 connections default)

### 3. Caching Opportunities (Future)
- Cache user roles (TTL 5 minutes)
- Cache project memberships
- Redis for session storage

### 4. Code-Level Optimizations
- Type hints for early error detection
- Pydantic validation at boundary
- Connection pooling configured

---

## Error Handling Strategy

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **204**: No Content
- **400**: Bad Request (validation error)
- **401**: Unauthorized (invalid credentials)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **500**: Server Error

### Example Error Response
```json
{
  "detail": "Not authorized to update this project",
  "error_code": "PERMISSION_DENIED"
}
```

### Exception Hierarchy
```
BaseException
├── HTTPException (FastAPI)
│   ├── 401 Unauthorized
│   ├── 403 Forbidden
│   └── 404 Not Found
├── ValueError (Business logic)
├── PermissionError (Authorization)
└── SQLAlchemy Exceptions
```

---

## Deployment Architecture

### Docker Layers
```
Stage 1: Builder
├── Install build dependencies
├── Install Python packages
└── Create wheels

Stage 2: Runtime
├── Install runtime dependencies only
├── Copy wheels from builder
├── Create non-root user
└── Health check configured
```

### Container Orchestration (Future)
```
Kubernetes
├── API Pod (replicas: 3)
├── PostgreSQL StatefulSet
├── Redis Cache (optional)
└── Monitoring/Logging
```

---

## Monitoring & Logging

### Health Checks
```
GET /api/v1/health
Response: {"status": "healthy"}
```

### Metrics to Track
- Response time by endpoint
- Error rates by status code
- Database query performance
- Authentication failure attempts
- Authorization denials

### Logging Points
- Authentication attempts (success/failure)
- Authorization denials
- Database errors
- Unexpected exceptions

---

## Future Enhancements

### Phase 2
- [ ] WebSocket support for real-time updates
- [ ] Email notifications on task updates
- [ ] Task comments & activity log
- [ ] Advanced filtering & search
- [ ] Task templates

### Phase 3
- [ ] Analytics dashboard
- [ ] Reporting capabilities
- [ ] API rate limiting
- [ ] Request signing for security
- [ ] OAuth2 third-party integration

### Phase 4
- [ ] Multi-tenancy
- [ ] Custom workflows
- [ ] Webhook support
- [ ] GraphQL API
- [ ] Mobile app backend

---

## Conclusion

This architecture demonstrates:
- ✅ **Clean Code**: Separation of concerns
- ✅ **Scalability**: Async/await for high concurrency
- ✅ **Security**: RBAC and JWT authentication
- ✅ **Testability**: Dependency injection and repositories
- ✅ **Maintainability**: Clear structure and documentation
- ✅ **Production-Ready**: Containerization and error handling

Perfect for portfolios, job interviews, and production deployments!
