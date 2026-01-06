# Magrathea Project Context

Magrathea is a Python-based map generation service. It uses FastAPI for the web interface and SQLAlchemy with SQLite for persistence.

## Key Technologies
- **Python 3.13+**
- **FastAPI**: Web framework for the API.
- **SQLAlchemy**: ORM for database interactions.
- **Noise/Perlin Noise (OpenSimplex)**: Used for procedural map generation.
- **Matplotlib/Pillow**: Used for rendering maps.
- **uv**: Modern Python package manager and runner.

## Project Structure
- `src/magrathea/`: Main source code.
- `src/magrathea/maps/`: Core logic for map generation and rendering.
- `tests/`: Unit and integration tests.
- `notebooks/`: Jupyter notebooks for experimentation and visualization.
- `.github/workflows/`: Gemini-powered GitHub Actions for PR reviews, issue triage, and more.

## Map Generation
- **Algorithms**: Implemented using OpenSimplex noise (via `opensimplex`) and Fractal Brownian Motion (FBM).
- **Location**: See `src/magrathea/maps/rendering_engine.py` for noise generation and heightmap logic.

## Key Endpoints
- `POST /maps`: Generate and store a new map (persisted in DB).
- `GET /maps/{id}`: Retrieve a stored map by ID.
- `GET /map`: Ephemeral map generation for quick testing (returns PNG directly, no DB storage).

## Development & Code Quality



To maintain consistency and high code quality, this project uses `ruff` and `mypy`. These tools are integrated into the workflow via `uv` and `prek`.



### Linting and Formatting (Ruff)

We use [Ruff](https://docs.astral.sh/ruff/) for extremely fast linting and formatting. It replaces Flake8, Black, and isort.

- **Check for lint errors**: `uv run ruff check .`

- **Fix fixable errors**: `uv run ruff check . --fix`

- **Format code**: `uv run ruff format .` (Equivalent to Black)



### YAML Formatting (yamlfix)

We use [yamlfix](https://github.com/lyz-code/yamlfix) for formatting YAML files.

- **Format YAML**: `uv run yamlfix .`



### Static Type Checking (Mypy)

We use [Mypy](https://mypy.readthedocs.io/) for static type hints.

- **Run type check**: `uv run mypy src`

- Note: Configuration is located in `pyproject.toml`.



### Automated Quality Checks (prek)

`prek` hooks are configured to run automatically before every commit.

- **Install hooks**: `uv run prek install`

- **Run all hooks manually**: `uv run prek run --all-files`



## Testing

We use `pytest` for testing.

- **Run tests**: `uv run pytest`

- **Watch mode (development)**: `uv run pytest-watcher .`



## Development Guidelines

- **Idiomatic Python**: Follow PEP 8 and use modern Python features (>= 3.13).

- **API Documentation**: Ensure all FastAPI endpoints have clear type hints and docstrings; they are automatically documented via Swagger at `/docs`.

- **Database**: Use SQLAlchemy for all database operations. Avoid raw SQL where possible.
    - **Migrations**: Use Alembic for all schema changes.
    - **Apply**: `uv run alembic upgrade head`
    - **Create**: `uv run alembic revision --autogenerate -m "..."`
    - **Note**: The app does not create tables on startup. You must run migrations manually.

- **Dependencies**: Always use `uv sync` to keep the environment updated and `uv add <package>` to add new dependencies.

- **Continuous Integration**: Every PR is checked via GitHub Actions for linting, type checking, and tests.



## Instructions for Gemini CLI

When assisting with this repository:

1.  **Always Format**: After modifying Python files, run `ruff format` and `ruff check --fix`. For YAML files, run `yamlfix .`.

2.  **Verify Types**: Run `mypy` to ensure no type regressions were introduced.

3.  **Run Tests**: Verify changes with `pytest` before proposing a plan completion.

4.  **Run Pre-commit Hooks**: Run `uv run prek run --all-files` to ensure all hooks pass.

5.  **Context**: Use the `src/magrathea/maps/` directory as the reference for procedural logic and `src/magrathea/main.py` for API routing.
