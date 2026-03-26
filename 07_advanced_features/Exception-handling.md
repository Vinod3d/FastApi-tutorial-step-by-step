#  Exception Handling

Exception handling in **FastAPI** is used to manage errors properly and return meaningful responses to the client instead of crashing the server.

When something goes wrong in your API:

* Invalid input
* Resource not found
* Authentication failure
* Database error

FastAPI allows you to handle these errors cleanly and professionally.

### 1️⃣ What is Exception Handling?

Exception handling means Catching errors and returning a proper response instead of breaking the application.

Example problem:

* User requests `/users/100`
* But user with ID 100 does not exist
* Instead of server crash → return clean error message


#### Basic Exception – HTTPException

FastAPI provides built-in class:

```python
from fastapi import HTTPException
```

#### Example 1: Simple Not Found Error

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_db = {1: "Vinod", 2: "Rahul"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {"user": fake_db[user_id]}
```

#### 🔎 Output if user not found:

```json
{
  "detail": "User not found"
}
```

### 2️⃣ Common HTTP Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 422  | Validation Error      |
| 500  | Internal Server Error |

---



### 3️⃣ Handling Validation Errors

FastAPI automatically validates input using Pydantic.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.post("/create")
def create_user(user: User):
    return user
```

If age is string → FastAPI returns:

```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

This error is generated automatically.

### 4️⃣ Custom Exception Class

You can create your own exception.

#### Step 1: Create Custom Exception

```python
class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
```

#### Step 2: Create Exception Handler

```python
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "User Not Found",
            "user_id": exc.user_id
        }
    )
```

#### Step 3: Use It

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise UserNotFoundException(user_id)
    return {"user": fake_db[user_id]}
```


### 5️⃣ Global Exception Handler

Catch all unexpected errors:

```python
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Something went wrong",
            "message": str(exc)
        }
    )
```

⚠ In production, avoid exposing real error message.


### 6️⃣ Handling RequestValidationError Manually

Import:

```python
from fastapi.exceptions import RequestValidationError
```

Example:

```python
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Failed",
            "details": exc.errors()
        }
    )
```

### 7️⃣ Returning Custom Response Directly

Instead of raising exception:

```python
from fastapi.responses import JSONResponse

@app.get("/test")
def test():
    return JSONResponse(
        status_code=400,
        content={"error": "Bad request"}
    )
```

### 8️⃣ Production-Level Best Practices

1. Do not expose internal errors
2. Use structured error format
3. Log errors properly
4. Create reusable custom exceptions
5. Separate error handlers in different file

Example structure:

```
app/
 ├── main.py
 ├── exceptions.py
 ├── handlers.py
```

### 9️⃣ Using Middleware for Exception Logging

```python
from starlette.middleware.base import BaseHTTPMiddleware
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print("Error:", e)
            raise e

app.add_middleware(LoggingMiddleware)
```