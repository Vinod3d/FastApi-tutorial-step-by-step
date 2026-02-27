# Response Models

Many beginners ignore this topic — but in interviews, this shows your maturity in API design.


## 1️⃣ What is a Response Model?

A response model defines:

* What data should be returned
* What fields should be hidden
* Output validation
* Automatic documentation in Swagger

It uses **Pydantic models**.

## 2️⃣ Why Response Model is Important?

Imagine database model:

```python
class UserDB(BaseModel):
    id: int
    name: str
    email: str
    password: str
```

If you return this directly:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": 1,
        "name": "Vinod",
        "email": "vinod@email.com",
        "password": "secret123"
    }
```

🚨 Problem:
You are exposing password publicly.

---

# 🔹 3️⃣ Solution: Use Response Model

Create a safe model:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

Then:

```python
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {
        "id": 1,
        "name": "Vinod",
        "email": "vinod@email.com",
        "password": "secret123"
    }
```

### 🔎 What happens?

FastAPI automatically:

* Filters out `password`
* Validates output
* Returns only allowed fields


# 🔥 Interview Point

Response model:

* Improves security
* Controls output shape
* Enforces data contract
* Prevents accidental data leaks

## 4️⃣ Response Model for List

```python
from typing import List

@app.get("/users", response_model=List[UserResponse])
def get_users():
    return [
        {
            "id": 1,
            "name": "Vinod",
            "email": "vinod@email.com",
            "password": "123"
        }
    ]
```

FastAPI removes `password` from each object.

## 5️⃣ Separate Models for Input & Output

Very common interview pattern.

```python
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

* `UserCreate` → Request body
* `UserResponse` → Response


## 6️⃣ Optional Response Fields

```python
class ProductResponse(BaseModel):
    name: str
    price: float
    description: str | None = None
```

## 7️⃣ Response Model Exclude / Include

```python
@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    response_model_exclude={"email"}
)
```

You can dynamically exclude fields.

## 8️⃣ Response Model with Status Code

```python
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "email": user.email
    }
```

# 🔥 Advanced Interview Concept

### ❓ Does FastAPI validate response data?

Yes.

If you return wrong type:

```python
return {
    "id": "wrong",   # should be int
    "name": "Vinod",
    "email": "email"
}
```

FastAPI will raise validation error.

## 9️⃣ ORM Mode

When using database models (like SQLAlchemy), enable ORM mode.

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
```

This allows returning database objects directly.

# 🔥 Response Model vs Returning Dict

| Without Response Model | With Response Model |
| ---------------------- | ------------------- |
| No filtering           | Auto filtering      |
| No output validation   | Output validation   |
| Risk of data leak      | Secure              |
| Weak API contract      | Strong API contract |

# 🚨 Common Mistakes

❌ Using same model for DB, input, and output
❌ Exposing password
❌ Not using response_model
❌ Ignoring output validation


# 🎯 Senior-Level Interview Question

**Why should we separate request and response models?**

Answer:

* Security
* Different validation rules
* Clean architecture
* Avoid exposing internal fields