# Advanced FastAPI Application Template

A modern, production-ready FastAPI application template with Docker support, following best practices for structure and clean code.

## Features

- 🚀 FastAPI with async support
- 🐳 Docker and Docker Compose configuration
- 🗄️ PostgreSQL database with async support
- 📝 SQLAlchemy ORM with async operations
- 🔄 Redis for caching
- 🔐 JWT Authentication
- 📚 Auto-generated API documentation
- ✨ CORS middleware configured
- 🧪 Testing setup with pytest
- 🎨 Code formatting with Black and isort
- 🔍 Linting with Flake8

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── items.py
│   │           └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── crud/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Create a `.env` file in the root directory (optional, default values are provided):
   ```env
   DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
   REDIS_URL=redis://redis:6379/0
   SECRET_KEY=your-secret-key-here
   ```

3. Build and start the services:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - API Base URL: http://localhost:8000/api/v1

## Development

### Running Tests
```bash
docker-compose exec api pytest
```

### Code Formatting
```bash
docker-compose exec api black .
docker-compose exec api isort .
```

### Linting
```bash
docker-compose exec api flake8
```

## API Documentation

The API documentation is automatically generated and can be accessed at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Components

### API Structure
- `app/api/v1/`: API version 1 endpoints
- `app/core/`: Core functionality (config, database)
- `app/crud/`: Database CRUD operations
- `app/models/`: SQLAlchemy models
- `app/schemas/`: Pydantic models for request/response

### Database
- Async PostgreSQL with SQLAlchemy
- Migrations handled by Alembic
- Redis for caching and session management

### Authentication
- JWT-based authentication
- Secure password hashing
- Role-based access control

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 