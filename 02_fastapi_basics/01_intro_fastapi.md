# Introduction to FastAPI




FastAPI is a modern high-performance Python web framework used to build RESTful APIs. It is built on top of Starlette and uses ASGI for asynchronous request handling. It also provides automatic data validation using Pydantic and generates API documentation automatically using OpenAPI and Swagger.

It stands on the shoulders of two giants:
1. **Starlette:** Handles the web parts (routing, requests, ASGI).
2. **Pydantic:** Handles the data parts (validation, serialization).


### 1. ASGI (Asynchronous Server Gateway Interface)
ASGI is a specification that allows asynchronous communication between Python web servers and applications.

**Key points:**
- Supports async programming 
- Handles multiple requests simultaneously
- Faster than WSGI
- Example frameworks using ASGI:
    - FastAPI
    - Starlette
    - Django Channels

### 2 Starlette
Starlette is a lightweight ASGI framework used by FastAPI.
**It provides:**
- High-speed routing
- Middleware support
- Background tasks
- WebSocket support
FastAPI is built on top of Starlette, which provides the core networking functionality.

### 3 Uvicorn
Uvicorn is an ASGI server used to run FastAPI applications.
Example command:
uvicorn main:app --reload

**Responsibilities of Uvicorn:**
- Run the application
- Handle HTTP requests
- Serve responses


## Code Example
There is no code for this conceptual intro, but this is the mental model you need:
```python
# A typical mental model of a FastAPI app
from fastapi import FastAPI
app = FastAPI()

# 1. Client sends Data -> 2. Pydantic Validates Data -> 3. Your Function Runs -> 4. FastAPI Returns JSON
```

## Why FastAPI is Faster than Flask and Django
Traditional frameworks like:
Flask
Django
are based on WSGI (Web Server Gateway Interface).
WSGI is synchronous, meaning:
One request is processed at a time.
FastAPI uses ASGI, which supports asynchronous programming.
Advantages:
- Handles multiple requests concurrently
- Non-blocking execution
- Higher throughput
- Better performance

## Fast Development in FastAPI
FastAPI speeds up development because it provides many built-in features.

### 1. Pydantic (Data Validation)
FastAPI uses Pydantic for automatic data validation.
Example:
If an API expects an integer but receives a string, FastAPI will automatically throw a validation error.
Benefits:
- Automatic request validation
- Automatic data parsing
- Type checking
Example:
from pydantic import BaseModel
```python
class User(BaseModel):
    name: str
    age: int
```

### 2. Serialization
Serialization converts Python objects into formats like JSON for API responses.
FastAPI automatically handles serialization using Pydantic models.
Example response:
```python
{
  "name": "Vinod",
  "age": 24
}
```

### 3. Automatic API Documentation
FastAPI automatically generates API documentation using OpenAPI standard.
Two built-in interfaces:
- **Swagger UI**
Access at:
/docs

Provides:
- Interactive API testing
- Request/response visualization
- **ReDoc**
Access at:
/redoc

Provides:
- Clean documentation interface
This removes the need to manually write API documentation.

## Key Features of FastAPI
1. High Performance: FastAPI is one of the fastest Python frameworks, comparable to NodeJS and Go.

2. Easy Development: Simple and readable syntax reduces development time.

3. Automatic API Documentation: Automatically generates OpenAPI and Swagger documentation.

4. Automatic Data Validation: Uses Pydantic to validate request data automatically.

5. Asynchronous Support: Supports async/await for high-performance applications.

6. Built-in Serialization: Automatically handles serialization using Pydantic models.


## Best Practices
- **Embrace Type Hints:** FastAPI's superpower is built around standard Python type hints (`name: str`, `age: int`). If you don't use type hints, you lose 90% of FastAPI's benefits.
- **Learn Async:** To get the true performance of FastAPI, understand `async` and `await` deeply.

## Common Mistakes
- **Treating it like Flask/Django:** FastAPI uses ASGI (asynchronous), while Flask traditionally uses WSGI (synchronous). You can't just copy-paste Flask architectural patterns and expect them to be efficient in FastAPI.
- **Ignoring Pydantic:** Manual data validation (e.g., `if type(age) != int: return error`) is an anti-pattern in FastAPI. Always let Pydantic handle it.

## Interview Questions
**Q: What is FastAPI built on?**
A: It is built on Starlette for web routing/ASGI support, and Pydantic for data validation and serialization.

**Q: Why is FastAPI considered one of the fastest Python frameworks?**
A: Because it utilizes ASGI (Asynchronous Server Gateway Interface) natively, allowing it to handle thousands of concurrent requests natively without blocking, similar to NodeJS or Go.
