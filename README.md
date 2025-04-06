# Python Microservice Template

A robust template for building Python-based microservices with FastAPI, SQLite, and Docker.

## Features

- **FastAPI Framework**: High-performance REST API with automatic OpenAPI documentation
- **SQLite Database**: Simple, file-based database with SQLModel ORM
- **Alembic Migrations**: Database schema version control
- **API Key Authentication**: Basic API key authentication system
- **Background Tasks Tracking**: Built-in task tracking system for long-running jobs
- **Docker Support**: Containerized deployment with Docker and docker-compose
- **Structured Project Layout**: Clean organization for service code and API endpoints

## Project Structure

```
├── alembic/               # Database migration files
├── api/                   # API code
│   ├── core/              # Core configuration and database setup
│   ├── models/            # SQLModel database models
│   ├── routes/            # API endpoints
│   └── main.py            # FastAPI application entry point
├── data/                  # Database and persistent data
├── service/               # Service business logic (add your service code here)
├── scripts/               # Utility scripts
├── .env                   # Environment variables (create from .env.example)
├── Dockerfile             # Docker container definition
├── docker-compose.yaml    # Docker compose services
├── entrypoint.sh          # Container entrypoint script
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Environment Variables

The template uses environment variables for configuration. Create a `.env` file based on the provided `.env.example`:

| Variable                  | Description                                                    | Default                                                        |
| ------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| `DB_INIT_MODE`            | Database initialization mode: `NONE`, `MIGRATE`, or `RECREATE` | `MIGRATE`                                                      |
| `DEFAULT_API_USER`        | Name for the default API user                                  | `some-name`                                                    |
| `DEFAULT_API_KEY`         | API key for authentication (should be secure and unique)       | `some-key-whatever-you-want-make-sure-it-is-secure-and-unique` |
| `DEFAULT_API_DESCRIPTION` | Description for the default API user                           | `some-description`                                             |

## Getting Started

### Local Development

1. Clone this repository
2. Create a `.env` file from `.env.example`
3. Install uv (if not already installed):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh  # On macOS/Linux
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  # On Windows
   ```
4. Initialize the database:
   ```
   uv run python -m alembic upgrade head
   uv run python -m api.initial_data
   ```
5. Run the service:
   ```
   uv run uvicorn api.main:app --reload --port 8006
   ```
   This command will create the `.venv` directory in the project root if it doesn't exist and automatically install all dependencies listed in `pyproject.toml`. For more details, visit the [official uv repository](https://github.com/astral-sh/uv).

### Docker Deployment

1. Create a `.env` file from `.env.example`
2. Build and start the container:
   ```
   docker-compose up -d
   ```

## API Endpoints

The microservice comes with the following pre-built endpoints:

- **Health Check**: `/health_check`
- **Tasks API**: `/tasks` - CRUD endpoints for managing background tasks
- **Users API**: `/users` - CRUD endpoints for managing API users/keys

All endpoints (except health check) require an API key to be passed via the `SERVICE-NAME-API-KEY` header.

## Adding Your Service Logic

1. Add your service code to the `service/` directory
2. Create new API routes in `api/routes/` as needed
3. Define new models in `api/models/` as required
4. Run migrations to update the database schema:
   ```
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

## Database Management

- Use `DB_INIT_MODE=MIGRATE` for regular updates (default)
- Use `DB_INIT_MODE=RECREATE` to completely reset the database
- Use `DB_INIT_MODE=NONE` to skip database initialization

## License

MIT License
