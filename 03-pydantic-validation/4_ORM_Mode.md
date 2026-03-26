

## ORM Mode & Pydantic with Databases

This is where Pydantic connects with **real database models** (like SQLAlchemy). Almost every FastAPI interview includes this concept.


## **1 Why Do We Need ORM Mode?**

In real applications:

* Database models are created using **ORM libraries** (like SQLAlchemy).
* These models are **Python classes**, not dictionaries.
* Pydantic normally expects **dict-like data**.

So how do we convert:

```
SQLAlchemy Model → Pydantic Model → JSON Response
```

👉 That’s where **ORM Mode** comes in.


## 2️ Problem Without ORM Mode

Let’s understand the issue.

### Example: SQLAlchemy Model

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

Now suppose you fetch a user from DB:

```python
user_from_db = UserDB(id=1, name="Vinod", email="vinod@example.com")
```

If you try:

```python
UserResponse(**user_from_db)
```

❌ It will fail.

Because `user_from_db` is **not a dictionary**.

## 3️ Solution: ORM Mode

Pydantic provides:

```python
class Config:
    orm_mode = True
```

(For Pydantic v2 → `model_config = ConfigDict(from_attributes=True)`)


## Example: Pydantic Response Model

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
```

Now you can do:

```python
user_pydantic = UserResponse.from_orm(user_from_db)
print(user_pydantic)
```

✅ It works perfectly.

## 4️ Real FastAPI Example (Complete Flow)

### Step 1: Database Model

```python
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

---

### Step 2: Pydantic Models

We usually create **two models**:

### 🔹 Request Model (for input)

```python
class UserCreate(BaseModel):
    name: str
    email: str
```

### 🔹 Response Model (for output)

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
```

### Step 3: FastAPI Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    db_user = UserDB(id=1, name=user.name, email=user.email)
    return db_user
```

Here:

* `UserCreate` → validates request body
* `UserResponse` → validates response
* `orm_mode=True` → allows returning SQLAlchemy object directly

## 5️ Why Separate Create and Response Models?

Very common interview question 🔥

Example:

```python
class UserCreate(BaseModel):
    name: str
    email: str
    password: str   # input only

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

We do NOT include password in response.

👉 This is called **Data Hiding / Secure API Design**

## 6️ Nested ORM Example (Advanced & Important)

Suppose we have:

### DB Models:

```python
class AddressDB(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String)
    user_id = Column(Integer)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = relationship("AddressDB")
```

### Pydantic Models:

```python
class AddressResponse(BaseModel):
    city: str
    country: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    address: AddressResponse

    class Config:
        orm_mode = True
```

Now FastAPI automatically:

```
UserDB object → UserResponse → JSON
```

Even nested relationships work correctly.

## 7️ Interview Important Points

You should confidently explain:

✅ What is ORM mode?
→ Allows Pydantic to read data from ORM objects (attributes instead of dict keys).

✅ Why use separate schemas?
→ Security, cleaner API design, control over input/output.

✅ What happens if orm_mode is missing?
→ FastAPI cannot serialize ORM objects correctly.

✅ Difference between:

* `.dict()`
* `.json()`
* `.from_orm()`

## 8️ Pydantic v2 Note

If interviewer asks about latest version:

Instead of:

```python
class Config:
    orm_mode = True
```

We use:

```python
from pydantic import BaseModel, ConfigDict

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
```

This replaces `orm_mode`.