# Setting Up a FastAPI Project

### Installing FastAPI
- Recommended: use a virtual environment (venv or poetry).

Install with pip:

```bash
python -m venv .venv
source .venv/bin/activate   # Unix/macOS
.venv\Scripts\activate    # Windows Powershell
pip install --upgrade pip
pip install "fastapi[standard]"
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

## Best Practices
- **Always use a Virtual Environment:** Never install dependencies globally. Use `venv`, `poetry`, or `pipenv`.
- **Pin Your Versions:** In your `requirements.txt`, always freeze the exact versions (e.g., `fastapi==0.103.1`) so your app doesn't break when deployed.

## Common Mistakes
- **Forgetting to activate the venv:** Installing packages and wondering why `import fastapi` fails because you installed them globally instead of in the virtual environment.
- **Not installing uvicorn:** FastAPI is just a framework. It CANNOT run by itself. It needs an ASGI server like Uvicorn to host it.

## Interview Questions
**Q: What is Uvicorn?**
A: Uvicorn is a lightning-fast ASGI (Asynchronous Server Gateway Interface) server that acts as the web server to run your FastAPI applications.

**Q: How do you isolate dependencies in a Python project?**
A: By using a Virtual Environment (`venv`). This ensures that the packages required for this specific project do not conflict with packages installed globally on the system or in other projects.
