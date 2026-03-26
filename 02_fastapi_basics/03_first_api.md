# Your First FastAPI App

## What you will learn
- Creating a basic FastAPI application instance
- Defining an endpoint with decorators
- Running the server with live reloading
- Exploring auto-generated interactive Swagger documentation

## Concept (Simple Explanation)
An API is simply an application waiting for a specific command.
- The **FastAPI instance** (`app = FastAPI()`) is the main building of your restaurant.
- The **Decorator** (`@app.get("/")`) is placing a sign on a specific door that says "To get the menu, come to this door."
- The **Function** underneath is the worker who hands out the menu when someone knocks.

## Code Example
Create a file named `main.py`:
```python
from fastapi import FastAPI

# Initialize the application instance
app = FastAPI(title="My First API", description="Learning FastAPI from scratch")

# Create a route handle for GET requests at the root ("/")
@app.get("/")
async def read_root():
    # FastAPI automatically serializes this dictionary into JSON!
    return {"message": "Hello, FastAPI! Welcome to backend development."}
```

**Run the app:**
```bash
# "main" is the filename, "app" is the variable name inside it.
# --reload automatically restarts the server when you save code changes.
uvicorn main:app --reload
```

## Best Practices
- **Use meaningful titles and descriptions:** When initializing `FastAPI()`, pass metadata like `title`, `description`, and `version`. This makes your auto-generated docs look professional immediately.
- **Use `--reload` only for development:** Never use the `--reload` flag in production environments. It consumes unnecessary resources.

## Common Mistakes
- **Running the file directly:** Beginners often try to run `python main.py`. That won't start the server. You MUST use `uvicorn main:app`.
- **Wrong module import string:** Writing `uvicorn app:main` instead of `main:app`. The syntax is `filename:fastapi_variable_name`.

## Interview Questions
**Q: How does FastAPI generate interactive API documentation automatically?**
A: By utilizing standard Python type hints and Pydantic, FastAPI generates an OpenAPI Schema behind the scenes. This schema is then utilized to render Swagger UI (`/docs`) and ReDoc (`/redoc`) automatically.

**Q: Explain the command `uvicorn main:app --reload`.**
A: `uvicorn` starts the ASGI server. `main` refers to the `main.py` file. `app` refers to the FastAPI instance declared inside that file. `--reload` tells the server to watch for file changes and restart automatically during development.
