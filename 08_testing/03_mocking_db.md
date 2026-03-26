# Dependency Overrides (Mocking the DB)

## What you will learn
- Why you should never test against a Production Database
- Using FastAPI's `app.dependency_overrides`
- Injecting a fake SQLite database for lightning-fast testing
- Mocking Authentication headers to test secure routes instantly

## Concept (Simple Explanation)
If your `POST /register` endpoint actually writes to your live production PostgreSQL database during a test, you will fill your real database with thousands of garbage test users.

In FastAPI, since everything is safely injected using `Depends()`, we can trick the application.
When the test runs, we tell FastAPI: *"Whenever any endpoint asks for the real `get_db` dependency, intercept it, and give them this fake SQLite in-memory database instead!"* The endpoint is entirely fooled, and testing becomes 100% safe.

## Code Example
**How to Override a Dependency for Testing**

Imagine your real dependency looks like this:
```python
from database import SessionLocal

def get_db():
    db = SessionLocal() # Connects to real MySQL
    try:
        yield db
    finally:
        db.close()
```

**In your `tests/conftest.py` or test file:**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base
from dependencies import get_db

# 1. Create an IN-MEMORY SQLite database. (It vanishes when the test ends!)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create the tables in the fake database
Base.metadata.create_all(bind=engine)

# 3. Define the Fake Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. OVERRIDE THE LIVE DEPENDENCY
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user_in_fake_db():
    # This request will now hit `override_get_db` instead of the real one!
    response = client.post("/users", json={"name": "test_guy", "email": "test@test.com"})
    assert response.status_code == 200
```

## Best Practices
- **Also override Authentication (`get_current_user`):** To test an endpoint protected by an Admin requirement, you don't need to actually write a login test, generate a JWT, and pass headers. Just override `get_current_user` to return `{"role": "admin"}` instantly!
- **Drop the database after testing:** Always ensure the test database tables are dropped or deleted after the test suite finishes so you don't leak "test.db" files into github.

## Common Mistakes
- **Forgetting `app.dependency_overrides.clear()`:** If you override a dependency for *one specific test*, it stays overridden for every test that runs after it. Always clear the overrides dictionary in a teardown block or at the end of the test explicitly if it isn't meant to be global.

## Interview Questions
**Q: How does FastAPI's DI (Dependency Injection) system make mocking databases easier than environments like Django?**
A: In Django or Flask, database connections are often deeply hardcoded or accessed globally. To mock them, you usually have to "Monkey-patch" system libraries, which is brittle. FastAPI routes explicitly declare their dependencies via `Depends(get_db)`. By simply replacing that specific dictionary key in `dependency_overrides`, the route accepts the mock natively without any patching.
