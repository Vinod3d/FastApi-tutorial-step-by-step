

#  Chapter 2: FastAPI Introduction & Setup



Comprehensive interview-ready notes for FastAPI setup, core concepts, and quick examples.

### Introduction
FastAPI is a modern, high-performance Python web framework for building APIs using standard Python type hints. It is built on top of Starlette (for the web parts) and Pydantic (for data validation).

### Installing FastAPI
- Recommended: use a virtual environment (venv or poetry).

Install with pip:

```bash
python -m venv .venv
source .venv/bin/activate   # Unix/macOS
.venv\Scripts\activate    # Windows Powershell
pip install --upgrade pip
pip install fastapi
```

### Installing Uvicorn
Uvicorn is a lightning-fast ASGI server commonly used to run FastAPI apps.

```bash
pip install "uvicorn[standard]"

# create requirement.txt file
pip freeze | Out-File -Encoding utf8 requirements.txt 
```

### First app
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
uvicorn app:app --reload
```

Notes:
- Use `--reload` during development to enable auto-reload on file changes.
- The import target `app:app` means `module_name:variable_name`.


### Interactive docs: Swagger UI and ReDoc
- FastAPI automatically exposes OpenAPI docs.
- Default routes:
	- Swagger UI: `/docs`
	- ReDoc: `/redoc`
	- OpenAPI JSON: `/openapi.json`

Customization:
- Provide metadata in `FastAPI()` constructor: `title`, `description`, `version`, `openapi_url`, `docs_url`, `redoc_url`.
- You can supply `openapi_tags` and `openapi_schema` overrides.

### Scalar API Documentation

```
pip install scalar-fastapi

```


```py
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
```

### Project structure

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