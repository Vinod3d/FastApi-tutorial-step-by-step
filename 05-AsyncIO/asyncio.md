

# Async I/O in FastAPI

## 1. What is Async I/O?

Async I/O (Asynchronous Input/Output) is a programming technique that allows a program to **perform other tasks while waiting for slow operations** like:

* Database queries
* API calls
* File reading/writing
* Network requests

Instead of blocking the entire program while waiting, async programs **continue executing other tasks**.

### Simple Idea

In synchronous code, the program waits for each task to finish before starting the next one.

In asynchronous code, the program can **start multiple tasks and handle them efficiently while waiting for results**.

---

# 2. Why FastAPI Uses Async I/O

FastAPI is built on **ASGI (Asynchronous Server Gateway Interface)** and supports asynchronous programming using **Python's asyncio library**.

Async programming allows FastAPI to:

* Handle **thousands of requests concurrently**
* Avoid blocking the server
* Improve performance for I/O operations
* Provide better scalability

---

# 3. Synchronous vs Asynchronous Execution

## Synchronous Example

```python
import time

def task():
    print("Start")
    time.sleep(3)
    print("End")

task()
```

Output:

```
Start
(wait 3 seconds)
End
```

The program **blocks for 3 seconds**.

---

## Asynchronous Example

```python
import asyncio

async def task():
    print("Start")
    await asyncio.sleep(3)
    print("End")

asyncio.run(task())
```

Here the program **does not block the event loop**.

---

# 4. Important Keywords

## async

Defines an asynchronous function.

```
async def function_name():
```

This function can run asynchronously.

---

## await

Used to wait for an asynchronous task to finish.

```
await some_async_function()
```

The program pauses this task but **continues executing other tasks**.

---

# 5. Async Functions in FastAPI

In FastAPI, endpoints can be defined using `async def`.

Example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello from FastAPI"}
```

This route is **asynchronous** and can handle multiple requests efficiently.

---

# 6. Example Using Async Sleep

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/wait")
async def wait_example():
    await asyncio.sleep(2)
    return {"message": "Response after 2 seconds"}
```

Explanation:

1. Client sends request
2. Server waits 2 seconds
3. Meanwhile server can handle other requests
4. Response is returned

---

# 7. Running Multiple Async Tasks

`asyncio.gather()` is used to run multiple async functions concurrently.

Example:

```python
import asyncio

async def task1():
    await asyncio.sleep(2)
    return "Task 1 completed"

async def task2():
    await asyncio.sleep(1)
    return "Task 2 completed"

async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)

asyncio.run(main())
```

Output:

```
['Task 1 completed', 'Task 2 completed']
```

Both tasks run **concurrently**.

---

# 8. Async External API Calls

Using `httpx` for asynchronous HTTP requests.

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/post")
async def get_post():

    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1")

    return response.json()
```

Advantages:

* Non-blocking request
* Faster API aggregation
* Better performance

---

# 9. Async Database Operations

Async database libraries allow queries without blocking.

Example concept:

```
Client Request
      ↓
FastAPI async route
      ↓
Async database query
      ↓
Return response
```

Libraries that support async database operations:

* async SQLAlchemy
* asyncpg
* databases library
* motor (MongoDB)

---

# 10. When to Use Async in FastAPI

Use `async def` when your endpoint performs:

* External API calls
* Database queries
* File uploads/downloads
* Network operations
* Waiting tasks

Example:

```
API → DB Query → API Call → Response
```

Async helps run these efficiently.

---

# 11. When NOT to Use Async

Do not use async when performing **CPU-heavy tasks**, such as:

* Image processing
* Data analysis
* Machine learning calculations
* Large computations

These should use:

* background tasks
* multiprocessing
* task queues

---

# 12. FastAPI Request Flow with Async

Request Flow:

```
Client Request
       ↓
FastAPI Route (async)
       ↓
Event Loop
       ↓
Async Task Execution
       ↓
Response Sent
```

The **event loop manages multiple requests efficiently**.

---

# 13. Advantages of Async in FastAPI

1. High performance
2. Handles multiple users simultaneously
3. Non-blocking operations
4. Efficient resource usage
5. Better scalability
6. Faster API response time
7. Ideal for I/O heavy applications

---

# 14. Disadvantages

1. Slightly more complex code
2. Debugging async code can be harder
3. Requires async-compatible libraries
4. Not useful for CPU-heavy operations

---

# 15. Simple FastAPI Async Example

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/task1")
async def task1():
    await asyncio.sleep(2)
    return {"message": "Task 1 completed"}

@app.get("/task2")
async def task2():
    await asyncio.sleep(1)
    return {"message": "Task 2 completed"}
```

Both routes can handle requests **without blocking each other**.

---

# 16. Real World Example (Dashboard API)

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

async def get_user():
    await asyncio.sleep(2)
    return {"name": "Vinod"}

async def get_orders():
    await asyncio.sleep(3)
    return {"orders": 5}

@app.get("/dashboard")
async def dashboard():

    user, orders = await asyncio.gather(
        get_user(),
        get_orders()
    )

    return {
        "user": user,
        "orders": orders
    }
```

Both tasks execute **in parallel**, reducing response time.

---

# 17. Key Points for Revision

* Async I/O allows programs to handle multiple operations efficiently.
* FastAPI supports async using `async def` and `await`.
* Async improves performance for **I/O-bound operations**.
* `asyncio` is the core Python library used for asynchronous programming.
* `asyncio.gather()` runs multiple tasks concurrently.
* Async is best suited for **network and database operations**.

---

# Short Interview Definition

**Async I/O in FastAPI allows handling multiple I/O-bound tasks concurrently using Python’s asyncio library. It enables non-blocking operations, improving the performance and scalability of APIs.**