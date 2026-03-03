# 🚀 Nexus Task Manager

**Enterprise-Grade Task & Resource Management System**

A production-ready FastAPI application demonstrating Senior-level software engineering practices with clean architecture, comprehensive testing, and professional deployment setup.

---

## ✨ Features

### 🔐 Authentication & Authorization
- **JWT-based OAuth2** authentication with access and refresh tokens
- **Role-Based Access Control (RBAC)** with Admin, Manager, and User roles
- **Secure password hashing** using bcrypt
- Token expiration and validation

### 📊 Core Functionality
- **Project Management**: Create, update, delete projects with ownership
- **Task Management**: Assign, track, and manage tasks with multiple statuses and priorities
- **User Management**: User profiles, team assignments, and permission control
- **Project Membership**: Team collaboration with granular permissions

### 🏗️ Architecture
- **Clean Architecture** (Hexagonal pattern)
- **Layered Design**: API → Services → Repositories → Database
- **Dependency Injection** using FastAPI's DI system
- **Async/Await** throughout for high performance
- **Type Safety** with Pydantic v2

### 📦 Database
- **PostgreSQL** with SQLAlchemy 2.0 (async)
- **Complex Relationships** with proper cascade deletion
- **Indexed Queries** for performance
- **Database Migrations** ready (Alembic)

### 🧪 Testing
- **>80% Test Coverage** with pytest
- **Unit Tests** for services and security
- **Integration Tests** for API endpoints
- **Authorization Tests** for RBAC verification
- **Async Test Support** with pytest-asyncio

### 🐳 DevOps
- **Docker & Docker Compose** for containerization
- **GitHub Actions CI/CD** with automated testing
- **Code Quality Checks** (Ruff, Black, MyPy)
- **Health Checks** configured

---

## 📁 Project Structure

```
nexus-task-manager/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py          # Router aggregation
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── users.py             # User management
│   │   │   ├── projects.py          # Project endpoints
│   │   │   ├── tasks.py             # Task endpoints
│   │   │   └── health.py            # Health check
│   │   └── dependencies.py          # DI & middleware
│   ├── core/
│   │   ├── config.py                # Pydantic Settings
│   │   ├── security.py              # JWT & password handling
│   │   ├── constants.py             # Enums & constants
│   │   └── database.py              # Async DB setup
│   ├── models/
│   │   ├── base.py                  # TimestampMixin & BaseModel
│   │   ├── user.py                  # User model with RBAC
│   │   ├── project.py               # Project model
│   │   ├── task.py                  # Task model
│   │   └── project_member.py        # Membership model
│   ├── repository/
│   │   ├── user_repository.py       # User data access
│   │   ├── project_repository.py    # Project data access
│   │   └── task_repository.py       # Task data access
│   ├── schemas/
│   │   └── __init__.py              # Pydantic validators
│   ├── services/
│   │   ├── auth_service.py          # Auth business logic
│   │   ├── user_service.py          # User business logic
│   │   ├── project_service.py       # Project business logic
│   │   └── task_service.py          # Task business logic
│   └── main.py                      # App factory
├── tests/
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_auth.py                 # Auth endpoints
│   ├── test_users.py                # User endpoints
│   ├── test_projects.py             # Project endpoints
│   ├── test_tasks.py                # Task endpoints
│   ├── test_health.py               # Health checks
│   └── test_security.py             # Security unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml                # GitHub Actions
├── Dockerfile                       # Container image
├── docker-compose.yml               # Dev environment
├── requirements.txt                 # Dependencies
├── .env.example                     # Env template
├── .gitignore                       # Git ignores
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (or use Docker)
- Docker & Docker Compose (optional but recommended)

### Local Development (with Docker)

**Fastest way to get running:**

```bash
# Clone repository
git clone <repo-url>
cd nexus-task-manager

# Start services
docker-compose up -d

# Check API is running
curl http://localhost:8000/api/v1/health
```

API will be available at `http://localhost:8000`  
Swagger UI: `http://localhost:8000/api/v1/docs`

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Start PostgreSQL (ensure it's running)

# Run application
python main.py
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (get tokens)
- `POST /api/v1/auth/refresh` - Refresh access token

### Users
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users/{user_id}` - Get user details
- `GET /api/v1/users` - List all users (admin only)
- `PUT /api/v1/users/{user_id}` - Update profile
- `DELETE /api/v1/users/{user_id}` - Deactivate user (admin only)

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List user's projects
- `GET /api/v1/projects/{project_id}` - Get project
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

### Tasks
- `POST /api/v1/projects/{project_id}/tasks` - Create task
- `GET /api/v1/projects/{project_id}/tasks` - List project tasks
- `GET /api/v1/projects/{project_id}/tasks/{task_id}` - Get task
- `PUT /api/v1/projects/{project_id}/tasks/{task_id}` - Update task
- `DELETE /api/v1/projects/{project_id}/tasks/{task_id}` - Delete task

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html -v
```

### Run Specific Test File
```bash
pytest tests/test_auth.py -v
```

### Run Tests with Markers
```bash
pytest tests/ -m asyncio -v
```

**Current Coverage**: >80% ✅

---

## 📝 Example Usage

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Create Project (with token)
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete redesign of company website"
  }'
```

### 4. Create Task in Project
```bash
curl -X POST http://localhost:8000/api/v1/projects/1/tasks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design new homepage",
    "description": "Create mockups for homepage",
    "priority": "high",
    "due_date": "2024-03-15T00:00:00"
  }'
```

---

## 🔒 Security Features

### ✅ Implemented
- JWT token-based authentication
- Password hashing with bcrypt
- Role-Based Access Control (RBAC)
- Authorization checks on all protected endpoints
- Input validation with Pydantic v2
- SQL injection protection via SQLAlchemy ORM
- CORS configuration
- HTTP security headers ready

### 🔐 Before Production
- Change `SECRET_KEY` in `.env`
- Use strong PostgreSQL passwords
- Enable HTTPS/TLS
- Set `DEBUG=false`
- Implement rate limiting
- Add request logging
- Configure proper CORS origins

---

## 📊 Code Quality

### Linting & Formatting
```bash
# Format code
black app/ tests/

# Lint check
ruff check app/ tests/

# Type checking
mypy app/
```

### GitHub Actions CI/CD
Automatically runs on every push:
- ✅ Unit & integration tests
- ✅ Code formatting (Black)
- ✅ Linting (Ruff)
- ✅ Type checking (MyPy)
- ✅ Coverage report

---

## 🗄️ Database

### Models Implemented
1. **User** - Authentication & RBAC
2. **Project** - Task collections with ownership
3. **Task** - Work items with status tracking
4. **ProjectMember** - Team management

### Relationships
```
User (1) ──→ (N) Project
User (1) ──→ (N) Task (as assignee)
Project (1) ──→ (N) Task
Project (1) ──→ (N) ProjectMember
User (1) ──→ (N) ProjectMember
```

### Migrations
Ready for Alembic integration:
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t nexus-task-manager:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/nexus \
  nexus-task-manager:latest
```

### Docker Compose
```bash
docker-compose up -d
docker-compose down
docker-compose logs -f api
```

---

## 📚 Technologies Used

| Category | Technology |
|----------|-----------|
| Framework | FastAPI 0.104+ |
| Web Server | Uvicorn |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 (async) |
| Validation | Pydantic v2 |
| Auth | Python-Jose (JWT) |
| Testing | Pytest, Pytest-asyncio |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Linting | Ruff, Black, MyPy |

---

## 🎯 Senior-Level Highlights

✅ **Clean Architecture** - Separation of concerns with proper layering  
✅ **RBAC & Authorization** - Fine-grained permission control  
✅ **Async/Await** - High-performance non-blocking I/O  
✅ **Comprehensive Testing** - >80% coverage with edge cases  
✅ **Type Safety** - Full type hints and validation  
✅ **Database Design** - Complex relationships & indexes  
✅ **Error Handling** - Proper HTTP status codes & messages  
✅ **Documentation** - Clear and professional  
✅ **CI/CD Ready** - Automated testing & deployment  
✅ **Production Ready** - Docker, health checks, security  

---

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Python JWT](https://pyjwt.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Submit pull request

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for aspiring Senior Developers**
