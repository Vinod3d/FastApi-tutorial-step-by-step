# Testing FastAPI with TestClient

## What you will learn
- How to test HTTP endpoints without actually running a live server
- Using FastAPI's `TestClient`
- Verifying JSON responses and HTTP Status Codes
- Testing POST requests and Validation Errors

## Concept (Simple Explanation)
Imagine you built an API endpoint: `GET /greeting`. To test it manually, you have to start Uvicorn, open Chrome, type `localhost:8000/greeting`, and look at the screen. Doing that 500 times after every code change is impossible.

FastAPI provides a **TestClient** (powered by Starlette and HTTPX). It spins up a fake, invisible version of your server entirely in memory. It perfectly simulates real network requests instantly, allowing you to prove your endpoints work in milliseconds.

## Code Example
**1. Your Application (`main.py`)**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 666:
        raise HTTPException(status_code=400, detail="Cursed Item")
    return {"item_id": item_id, "status": "Available"}
```

**2. Your Testing File (`tests/test_api.py`)**
```python
from fastapi.testclient import TestClient
from main import app  # Import your actual FastAPI application!

# Create the test client exactly once
client = TestClient(app)

def test_read_item_success():
    # Send a simulated HTTP GET request
    response = client.get("/items/10")
    
    # Assert the correct HTTP Status Code
    assert response.status_code == 200
    
    # Assert the actual JSON response body
    assert response.json() == {"item_id": 10, "status": "Available"}

def test_read_item_cursed():
    # Send a simulated request to a known failure path
    response = client.get("/items/666")
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Cursed Item"}
    
def test_read_item_validation_error():
    # Send a string to an endpoint demanding an INT
    response = client.get("/items/apple")
    
    # Prove that Pydantic properly blocks the invalid request!
    assert response.status_code == 422
```

## Best Practices
- **Use Pytest Fixtures for the TestClient:** If you have 20 test files, don't instantiate `client = TestClient(app)` 20 times. Put it in `conftest.py` as a fixture:
  ```python
  @pytest.fixture
  def client():
      return TestClient(app)
  ```
- **Test the failures, not just the successes:** Proving that your API returns a `200` is easy. The mark of a Senior Developer is proving that your API correctly returns a `422` when a user sends a missing email field, or a `404` when the user requests an ID that doesn't exist.

## Common Mistakes
- **Starting Uvicorn before running Pytest:** You do *not* need to run your live server to use `TestClient`. The client circumvents the network entirely and calls the FastAPI ASGI app directly in memory.

## Interview Questions
**Q: How does `TestClient` improve unit testing speed?**
A: `TestClient` simulates HTTP requests directly against the ASGI interface in memory. Because it bypasses real network I/O, physical port bindings (like localhost:8000), and actual HTTP serialization over TCP, it can run thousands of requests per second.

**Q: If a Pydantic model fails validation during a `TestClient` POST request, what status code should you assert?**
A: You should assert that `response.status_code == 422` (Unprocessable Entity), which is FastAPI's native response for schema validation failures.
