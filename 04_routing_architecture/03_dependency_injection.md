# Dependency Injection in FastAPI

## What you will learn
- What Dependency Injection (DI) actually is
- Using the `Depends()` function in FastAPI
- Sharing reusable logic (like Database connections and Authentication)
- `yield` dependencies and cleanups

## Concept (Simple Explanation)
Imagine you are building a LEGO set, and you need a special wrench. Instead of building the wrench yourself every time you need it, you just hold out your hand, and a helper places the exact wrench you need into it.

**Dependency Injection (DI)** is asking FastAPI to give your function something it needs to run. 
Instead of your endpoint opening a database connection manually, your endpoint tells FastAPI: *"Hey, I depend on a database connection."* FastAPI creates it, hands it to your endpoint, and cleans it up when the endpoint finishes.

## Code Example
```python
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# 1. Define a Dependency Function
def verify_token(token: str):
    if token != "supersecret":
         # If the dependency fails, the endpoint never even runs!
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": "admin"}

# 2. Inject the Dependency into a route
@app.get("/secure-data")
async def get_secure_data(user_data: dict = Depends(verify_token)):
    # This code only executes if verify_token succeeds.
    return {"data": "Highly classified info", "accessed_by": user_data}

# 3. 'Yield' Dependency (Great for Database Connections!)
def get_db():
    db = "Database_Connection_Opened"
    try:
        yield db  # Pauses here, gives the DB to the endpoint
    finally:
        # Executes AFTER the endpoint is totally finished, ensuring cleanup!
        print("Database_Connection_Closed")
```

## Best Practices
- **Use Dependencies for Database Sessions:** Always write a `get_db()` dependency using `yield` so that your database sessions are isolated per request and reliably closed, preventing memory leaks.
- **Use Dependencies for Auth:** Injecting `get_current_user` allows you to write the authentication logic once, and reuse it across 50 different secure endpoints simply by adding `user = Depends(get_current_user)`.

## Common Mistakes
- **Executing the dependency recursively:** Writing `Depends(verify_token())` (with the parentheses) is a fatal error. You must pass the *function reference*, not invoke it. Write: `Depends(verify_token)`. 
- **Confusing `Depends` with ordinary function calls:** A standard function runs exactly when you call it. A FastAPI Dependency is managed by the framework, injected at the start of the request, and its results can be cached if used multiple times in the same request.

## Interview Questions
**Q: Explain what Dependency Injection is and why FastAPI uses it.**
A: DI is a design pattern where a function receives its requirements from an external source rather than creating them itself. FastAPI uses it to share logic, enforce authentication, and manage resources like database sessions elegantly without repeating code.

**Q: What is a `yield` dependency in FastAPI?**
A: A `yield` dependency acts as a context manager. Code before the `yield` runs before the API endpoint executes (e.g., opening a DB connection). The `yield` hands the resource to the endpoint. The code after the `yield` runs after the endpoint finishes, ensuring safe teardown (e.g., closing the DB connection).
