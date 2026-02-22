<h1 style="color: #0ea5e9;  font-size: 40px; font-weight: bold;">
  Chapter 2: FastAPI Introduction & Setup
</h1>


Comprehensive interview-ready notes for FastAPI setup, core concepts, and quick examples.

## Introduction
FastAPI is a modern, high-performance Python web framework for building APIs using standard Python type hints. It is built on top of Starlette (for the web parts) and Pydantic (for data validation).

## Installing FastAPI
- Recommended: use a virtual environment (venv or poetry).

Install with pip:

```bash
python -m venv .venv
source .venv/bin/activate   # Unix/macOS
.venv\\Scripts\\activate    # Windows Powershell
pip install --upgrade pip
pip install fastapi
```

## Installing Uvicorn
Uvicorn is a lightning-fast ASGI server commonly used to run FastAPI apps.

```bash
pip install "uvicorn[standard]"
```

## First app
Create `app.py`:

```py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
		return {"message": "Hello, FastAPI!"}
```

Run it with Uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Notes:
- Use `--reload` during development to enable auto-reload on file changes.
- The import target `app:app` means `module_name:variable_name`.

## Running server & auto-reload
- Production should use process managers (systemd, containers) and optionally a process supervisor (Gunicorn with Uvicorn workers).
- For development use `uvicorn --reload` or `python -m uvicorn`.

## Auto reload internals
- `--reload` watches files and restarts the process when source files change.
- Works well for development but not production.

## Interactive docs: Swagger UI and ReDoc
- FastAPI automatically exposes OpenAPI docs.
- Default routes:
	- Swagger UI: `/docs`
	- ReDoc: `/redoc`
	- OpenAPI JSON: `/openapi.json`

Customization:
- Provide metadata in `FastAPI()` constructor: `title`, `description`, `version`, `openapi_url`, `docs_url`, `redoc_url`.
- You can supply `openapi_tags` and `openapi_schema` overrides.

## Project structure (recommended minimal layout)

```
project/
├─ app/
│  ├─ main.py        # FastAPI app instance and app startup
│  ├─ api/
│  │  ├─ v1/
│  │  │  ├─ endpoints.py
│  ├─ core/
│  │  ├─ config.py
│  ├─ models/
│  ├─ db/
│  └─ schemas/
├─ tests/
├─ requirements.txt
├─ pyproject.toml
└─ Dockerfile
```

Guidelines:
- Keep `app` creation in a single module (`main.py`) and import that module when running Uvicorn.
- Separate routers, models, schemas, and services for maintainability.

## ASGI explanation (short, interview-ready)
- ASGI (Asynchronous Server Gateway Interface) is the asynchronous successor to WSGI.
- It defines a standard interface between async Python web servers, frameworks, and apps.
- ASGI supports long-lived connections (WebSockets) and background tasks.
- FastAPI is an ASGI framework; Uvicorn is an ASGI server.

Key differences WSGI vs ASGI:
- WSGI: synchronous, one request per thread/process, used by frameworks like Flask and Django (classic).
- ASGI: supports async, concurrency with `async`/`await`, WebSockets, and streaming.

## Common pitfalls and best practices
- Avoid using blocking calls inside `async` endpoints — offload to thread pool (`run_in_executor`) or use async libraries.
- Keep heavy startup work out of module import time; use startup event handlers.
- Pin dependencies in `requirements.txt` for reproducible installs.

## Useful commands

```bash
# Run dev server
uvicorn app.main:app --reload

# Linting and formatting
pip install black ruff isort
black .

# Run tests
pytest -q
```

## Interview-style Q&A (short answers)

- Q: What is FastAPI?
	A: A modern, high-performance Python web framework that uses type hints for validation and documentation.

- Q What is a Virtual Environment in Python?

	A: A virtual environment is an isolated workspace where you can install Python packages separately for each project.

	In simple words, it creates a separate mini-Python setup inside your project folder.
	Whatever libraries you install inside it will not affect other projects or your main system Python.

	Python provides a built-in tool called venv to create virtual environments.

- Q: Why type hints matter in FastAPI?
	A: They enable automatic request parsing, validation with Pydantic, and auto-generated OpenAPI docs.

- Q: How do you run a FastAPI app in production?
	A: Use an ASGI server like Uvicorn (or Gunicorn with Uvicorn workers), run in Docker or managed process, configure logging and environment variables.

- Q: What is the purpose of `--reload` and should it be used in production?
	A: `--reload` restarts the server on code changes for developer convenience — do not use in production.

- Q: How are docs generated?
	A: FastAPI builds an OpenAPI schema from type hints and path operations; Swagger UI and ReDoc are auto-mounted.

- Q: Explain ASGI in one sentence.
	A: ASGI is an async interface standard that allows Python web apps to handle HTTP and WebSocket connections asynchronously.

## Sample interview exercises

1. Create a small FastAPI app with one GET and one POST endpoint, return validated Pydantic models.
2. Add a middleware that logs request method and URL.
3. Run the app with `uvicorn` and show that `/docs` works.
