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
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Example environment variables
├── .git/                  # Git repository files
├── .gitignore             # Git ignore file
├── .python-version        # Python version file (if used)
├── data/                  # Database and persistent data
├── service/               # Service business logic (add your service code here)
├── api/                   # API code, configuration, and dependencies
│   ├── Dockerfile         # Docker container definition for API
│   ├── alembic.ini        # Alembic configuration
│   ├── docker-compose.yaml # Docker compose (if API is run standalone, adjust as needed)
│   ├── pyproject.toml     # API project dependencies
│   ├── scripts/           # Utility scripts specific to the API
│   ├── src/               # API source code
│   │   ├── alembic/       # Database migration files
│   │   ├── core/          # Core configuration and database setup
│   │   ├── models/        # SQLModel database models
│   │   ├── routes/        # API endpoints
│   │   ├── __init__.py
│   │   ├── api.py         # API router setup
│   │   ├── deps.py        # FastAPI dependencies
│   │   ├── initial_data.py # Initial data seeding script
│   │   └── main.py        # FastAPI application entry point
│   └── uv.lock            # Lock file for API dependencies
├── docker-compose.yaml    # Main Docker compose services (references api context)
├── LICENSE                # Project License
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
4. Initialize the database (run from the project root):
   ```bash
   cd api
   uv run python -m alembic upgrade head
   uv run python -m src.initial_data
   cd ..
   ```
5. Run the service (run from the project root):
   ```bash
   cd api
   uv run uvicorn src.main:app --reload --port 8000 # Port mapped to 8006 by docker-compose
   cd ..
   ```
   The `uv run` command within the `api` directory will create the `.venv` directory there if it doesn't exist and automatically install all dependencies listed in `api/pyproject.toml`. For more details, visit the [official uv repository](https://github.com/astral-sh/uv).

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

1. Add your service code to the `service/` directory.
2. Create new API routes in `api/src/routes/` as needed.
3. Define new models in `api/src/models/` as required.
4. Run migrations to update the database schema (run from the project root):
   ```bash
   cd api
   alembic revision --autogenerate -m "Your migration message"
   alembic upgrade head
   cd ..
   ```

## Database Management

- Use `DB_INIT_MODE=MIGRATE` for regular updates (default)
- Use `DB_INIT_MODE=RECREATE` to completely reset the database
- Use `DB_INIT_MODE=NONE` to skip database initialization

## License

MIT License
