# Middleware in FastAPI

## What you will learn
- What Middleware is and where it sits in the Request Lifecycle
- How to create custom `BaseHTTPMiddleware`
- Understanding Callables and `call_next`
- Common use cases (Logging, Timeouts, CORS)

## Concept (Simple Explanation)
Imagine an international airport. Before a passenger (Request) can reach their airplane seat (Your API Endpoint), they must pass through Security. When they leave the plane (Response), they must pass through Customs.

**Middleware** is exactly that. It is a piece of code that runs *before* the request hits your router, and *after* the router generates a response. It sits right in the middle. You can use it to log every single request, add custom security headers, or block rogue IP addresses globally without modifying a single line of your actual endpoint code.

## Code Example
**1. Creating Custom Middleware (`main.py`)**
```python
import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Code here runs BEFORE the endpoint is reached (Airport Security)
        start_time = time.time()
        
        # 2. 'call_next' literally passes the request to your actual endpoint
        response = await call_next(request)
        
        # 3. Code here runs AFTER the endpoint finishes (Airport Customs)
        process_time = time.time() - start_time
        
        # Add a custom header to the final response showing how fast it was
        response.headers["X-Process-Time"] = str(process_time)
        return response

# Register the middleware globally
app.add_middleware(ProcessTimeMiddleware)

@app.get("/")
async def home():
    # Simulate a slow database query
    time.sleep(1)
    return {"message": "Hello World"}
```

**2. Built-in CORS Middleware**
If your React frontend runs on `localhost:3000` and FastAPI runs on `localhost:8000`, the browser will block the connection. You must use CORS middleware to fix this:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React app URL
    allow_credentials=True,
    allow_methods=["*"], # Allow GET, POST, DELETE, etc.
    allow_headers=["*"], # Allow Authorization headers
)
```

## Best Practices
- **Do not put heavy database queries in Middleware:** Middleware runs on *every single request* across your entire app (even checking a simple `/health` endpoint). If your middleware runs a 2-second database query, your entire application is now 2 seconds slower.
- **Use standard Starlette Middlewares when possible:** FastAPI is built on Starlette, which includes native middlewares for CORS, TrustedHosts, and GZipCompression. Use them instead of writing your own.

## Common Mistakes
- **Forgetting `await call_next(request)`:** If you forget to call and return `call_next()`, you are explicitly dropping the request. The user will simply receive a frozen connection or a 500 server error because the request never actually reached the router!

## Interview Questions
**Q: During the lifecycle of a request, when exactly does Middleware execute?**
A: Middleware executes twice. First, immediately after the server receives the raw HTTP request (before routing or validation occurs). Second, immediately after the router returns the HTTP response (before it is sent back to the client over the network).

**Q: What is the risk of reading the `request.body()` inside of a Middleware?**
A: In Starlette/FastAPI, the request body is an asynchronous stream. If you read the stream inside the middleware (e.g., to log the JSON payload), the stream is consumed/emptied. When the request finally reaches the FastAPI Endpoint, the body will be totally empty, causing a validation crash! You must carefully copy the byte stream if you need to read it in middleware.
