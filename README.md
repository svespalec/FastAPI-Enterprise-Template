# Advanced FastAPI Application Template

A modern, production-ready FastAPI application template with Docker support, following best practices for structure and clean code.

## Features

- 🚀 FastAPI with async support
- 🐳 Docker and Docker Compose configuration
- 🗄️ PostgreSQL database with async support
- 📝 SQLAlchemy ORM with async operations
- 🔐 JWT Authentication
- 📚 Auto-generated API documentation
- ✨ CORS middleware configured
- 🧪 Testing setup with pytest
- 🎨 Code formatting with Black and isort
- 🔍 Linting with Flake8
- 🔄 Continuous Integration with GitHub Actions

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
   git clone https://github.com/svespalec/FastAPI-Enterprise-Template.git
   ```

2. Create a `.env` file in the root directory (optional, default values are provided):
   ```env
   DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
   SECRET_KEY=your-secret-key-here
   ```

3. Build and start the services:
   ```bash
   docker compose up --build -d
   ```

4. Access the application:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - API Base URL: http://localhost:8000/api/v1

## Development

### Running Tests

You have multiple options to run tests:

#### Using Docker (Recommended for Development)
```bash
# Run all tests
docker compose run --rm test

# Run specific test file
docker compose run --rm test pytest tests/test_api.py -v

# Run specific test function
docker compose run --rm test pytest tests/test_api.py::test_create_user -v
```

#### Direct Command Line
```bash
pytest -v
```

### Code Quality

You can run code quality checks in two ways:

#### Using Docker (Recommended)
```bash
# Format code with Black and isort
docker compose run --rm format

# Check code style with Flake8
docker compose run --rm lint
```

#### Direct Command Line
```bash
# Format code
black .
isort .

# Check code style
flake8
```

## Continuous Integration

This template includes a GitHub Actions workflow that automatically:

1. **Runs on**:
   - Every push to master branch
   - Every pull request to master branch

2. **Test Job**:
   - Sets up Python 3.11
   - Spins up PostgreSQL for testing
   - Installs dependencies
   - Runs linting (flake8)
   - Checks formatting (black and isort)
   - Runs all tests (pytest)

3. **Build Job**:
   - Only runs after successful tests
   - Only on master branch pushes
   - Builds Docker image
   - Verifies build succeeds
   - Uses GitHub Actions cache for faster builds

## Deployment

This template is ready for deployment, but deployment itself depends on your needs. Here are some considerations:

### Production Requirements
- HTTPS/TLS setup
- Process management and auto-restart
- Load balancing
- Database backups
- Monitoring and logging
- Resource scaling

### Deployment Options
1. **Cloud Platforms**:
   - AWS (ECS, EKS)
   - Google Cloud (GKE)
   - Azure (AKS)
   - Digital Ocean
   - Hetzner
2. **Platform as a Service**:
   - Heroku
   - Google App Engine
   - Azure App Service

3. **Self-Hosted**:
   - Docker Swarm
   - Kubernetes
   - Traditional VM deployment

Choose your deployment platform based on:
- Scale requirements
- Budget constraints
- Team expertise
- Regulatory requirements
- Geographic distribution needs

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
- Clean async database operations

### Authentication
- JWT-based authentication
- Secure password hashing
- Role-based access control

### Testing
- Separate test database
- Async test client
- Automatic database cleanup between tests
- CI/CD integration via GitHub Actions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests and code quality checks:
   ```bash
   docker compose run --rm test
   docker compose run --rm format
   docker compose run --rm lint
   ```
4. Commit your changes
5. Push to the branch
6. Create a new Pull Request

## License

This project is licensed under the MIT License. 
