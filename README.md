# Magrathea

[![CI](https://github.com/BillyUdders/Magrathea/actions/workflows/ci.yml/badge.svg)](https://github.com/BillyUdders/Magrathea/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/release/python-3130/)

Magrathea is a FastAPI-based map generation service. It generates procedural maps and stores them in a local SQLite database.

## Features
- Procedural map generation using Perlin noise.
- API endpoints to create and retrieve maps.
- Persistence using SQLAlchemy and SQLite.

## Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Magrathea
   ```
2. Install dependencies:
   ```bash
   uv sync
   ```

### Running the Application
Start the FastAPI server using `uv`:
```bash
uv run uvicorn magrathea.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Documentation (Swagger)
Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Manual Testing with Swagger
1. Open the [Swagger UI](http://127.0.0.1:8000/docs).
2. Locate the `POST /maps` endpoint and click **Try it out**.
3. Modify the request body if desired (e.g., change `size` or `octaves`):
   ```json
   {
     "size": 128,
     "octaves": 4
   }
   ```
4. Click **Execute**. You will receive a response containing an `id` and a `url`.
5. Locate the `GET /maps/{map_id}` endpoint and click **Try it out**.
6. Paste the `id` from the previous step into the `map_id` field.
7. Click **Execute**. The response body will contain the generated image, and you can see a preview in the "Response body" section of Swagger.

## Development

### Pre-commit Hooks
This project uses `pre-commit` to ensure code quality. To set it up:
```bash
uv run pre-commit install
```
The hooks will run automatically on every commit. You can also run them manually:
```bash
uv run pre-commit run --all-files
```

### Type Checking
To run static type checking with `mypy`:
```bash
uv run mypy src
```

## Running Tests
To run the test suite, use `pytest`:
```bash
uv run pytest
```
This will execute the unit tests located in the `tests/` directory, verifying the API endpoints and map generation logic.
