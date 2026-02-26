# Decorators in FastAPI – Detailed Notes (Learning + Interview Perspective)

---

## 1️⃣ What is a Decorator in Python?

A **decorator** is a function that modifies or enhances another function **without changing its original code**.

It uses the `@` symbol.

### Basic Example (Python)

```python
def my_decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@my_decorator
def say_hello():
    print("Hello")

say_hello()
```

👉 Output:

```
Before function call
Hello
After function call
```

### Interview Definition

A decorator is a higher-order function that takes another function as input and returns a modified function as output.

---

# 2️⃣ Why Decorators Are Important in FastAPI?

In FastAPI, decorators are used to:

* Define routes
* Add metadata
* Handle dependencies
* Add validation
* Implement security
* Apply middleware-like logic

FastAPI heavily relies on decorators to make APIs clean and readable.

---

# 3️⃣ Route Decorators in FastAPI

FastAPI provides route decorators like:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* `@app.patch()`

These decorators register a function as an API endpoint.

---

## Example 1: Basic Route Decorator

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### What Happens Internally?

* `@app.get("/")` tells FastAPI:

  * This function handles GET requests
  * Path = "/"
  * Register it in routing table

### Interview Point

`@app.get()` is a decorator that registers the function as a route handler in FastAPI’s routing system.

---

# 4️⃣ How FastAPI Decorators Work Internally

Behind the scenes:

```python
@app.get("/items")
def get_items():
    return {"items": []}
```

Is equivalent to something like:

```python
def get_items():
    return {"items": []}

app.get("/items")(get_items)
```

👉 That means:

* `app.get("/items")` returns a decorator function
* That decorator function takes `get_items` as argument
* It registers it internally

---

# 5️⃣ Decorators with Parameters

FastAPI route decorators accept many parameters:

```python
@app.get(
    "/users",
    response_model=list[str],
    status_code=200,
    tags=["Users"],
    summary="Get all users",
    description="Returns a list of users"
)
def get_users():
    return ["Alice", "Bob"]
```

### Important Parameters

| Parameter        | Purpose                           |
| ---------------- | --------------------------------- |
| `response_model` | Validates and serializes response |
| `status_code`    | Sets HTTP status code             |
| `tags`           | Groups endpoints in Swagger UI    |
| `summary`        | Short API description             |
| `description`    | Detailed API description          |

---

# 6️⃣ Dependency Injection Using Decorators

FastAPI supports dependency injection using `Depends()`.

```python
from fastapi import Depends

def common_params(q: str = None):
    return {"q": q}

@app.get("/items/")
def read_items(commons: dict = Depends(common_params)):
    return commons
```

### What Happens?

* `Depends(common_params)` tells FastAPI:

  * Execute `common_params`
  * Inject its return value

### Interview Answer

FastAPI uses dependency injection via the `Depends()` system, which works together with route decorators to inject reusable logic.

---

# 7️⃣ Custom Decorators in FastAPI

You can also create your own decorators.

### Example: Logging Decorator

```python
from functools import wraps

def log_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("Function called")
        return await func(*args, **kwargs)
    return wrapper
```

Use it:

```python
@app.get("/hello")
@log_decorator
async def say_hello():
    return {"message": "Hello"}
```

⚠ Important:

* Use `async` wrapper if decorating async functions
* Always use `@wraps(func)`

---

# 8️⃣ Order of Decorators in FastAPI

Order matters.

Correct:

```python
@app.get("/test")
@custom_decorator
async def test():
    return {"msg": "ok"}
```

Execution flow:

1. `@custom_decorator` wraps function
2. `@app.get()` registers the wrapped function

Wrong order can cause issues.

---

# 9️⃣ Decorators vs Middleware in FastAPI

| Decorator                     | Middleware                          |
| ----------------------------- | ----------------------------------- |
| Applied to specific route     | Applied globally                    |
| Used for endpoint-level logic | Used for request/response lifecycle |
| Lightweight                   | More powerful                       |

Example Middleware:

```python
@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    return response
```

Interview Tip:
Use decorators for route-specific behavior, middleware for global processing.

---

# 🔟 Async Support in Decorators

FastAPI supports:

* `def` (sync)
* `async def` (async)

When creating custom decorators for FastAPI:

If route function is async → wrapper must be async.

Wrong:

```python
def wrapper():
    return func()
```

Correct:

```python
async def wrapper(*args, **kwargs):
    return await func(*args, **kwargs)
```

---

# 1️⃣1️⃣ Security Decorators in FastAPI

Security also works via dependencies.

Example with OAuth2:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Here:

* `Depends()` + security scheme works like a decorator-based injection system.

---

# 1️⃣2️⃣ Common Interview Questions

### Q1: What is a decorator?

A function that modifies another function without changing its source code.

### Q2: How does FastAPI use decorators?

To register routes, add metadata, inject dependencies, and handle validation.

### Q3: What is the difference between decorator and middleware?

Decorator works at route level, middleware works globally.

### Q4: Why is @wraps important?

It preserves original function metadata (name, docstring).

### Q5: What happens when you write @app.get("/")?

It registers that function in FastAPI’s internal routing system.

---

# 1️⃣3️⃣ Real-World Use Cases of Decorators in FastAPI

* Logging
* Authentication
* Role-based access control
* Caching
* Rate limiting
* Performance measurement
* Custom validation

---

# 1️⃣4️⃣ Summary (Important for Interview)

* FastAPI heavily depends on decorators
* Route decorators register endpoints
* Decorators can accept parameters
* Dependency injection works with decorators
* Order of decorators matters
* Async support must be handled carefully
* Middleware is different from decorators

---

If you want, I can next explain:

* Advanced decorator patterns in FastAPI
* How FastAPI internally builds routing system
* How to build production-ready custom decorators
* Decorator + Dependency injection deep dive
* Common mistakes in FastAPI decorators

Tell me which level you want next 🚀
