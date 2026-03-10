## 📌 1. Creating Models in SQLAlchemy

Now we will create **database tables using SQLAlchemy models**.

In ORM, a **Python class represents a database table**.

### Mapping Concept

| Database | Python          |
| -------- | --------------- |
| Table    | Class           |
| Column   | Class Attribute |
| Row      | Object          |

Example database table:

| id | name  | email                                     |
| -- | ----- | ----------------------------------------- |
| 1  | Vinod | [vinod@gmail.com](mailto:vinod@gmail.com) |

Equivalent Python object:

```python
user.id
user.name
user.email
```

---

#### Step 1: Create `models.py`

File location:

```
app/models.py
```

Import required modules.

```python
from sqlalchemy import Column, Integer, String
from .database import Base
```

#### Step 2: Create User Model

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
```


### Explanation

#### Table Name

```python
__tablename__ = "users"
```

This tells SQLAlchemy that the table name is:

```
users
```

#### ID Column

```python
id = Column(Integer, primary_key=True, index=True)
```

Explanation:

| Parameter        | Meaning                     |
| ---------------- | --------------------------- |
| Integer          | data type                   |
| primary_key=True | unique identifier           |
| index=True       | improves search performance |


#### Name Column

```python
name = Column(String(100))
```

Meaning:

```
VARCHAR(100)
```

in MySQL.

#### Email Column

```python
email = Column(String(100), unique=True, index=True)
```

Explanation:

| Property    | Meaning            |
| ----------- | ------------------ |
| unique=True | no duplicate email |
| index=True  | faster queries     |

### How ORM Converts Model to SQL

SQLAlchemy automatically converts the model into SQL table.

Equivalent MySQL query:

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
```

## 📌 2. Creating Database Tables

Now we create tables in MySQL using SQLAlchemy.

Go to **main.py**.

## Import Models and Base

```python
from fastapi import FastAPI
from app.database import engine
from app import models
```

---

## Create Tables

```python
models.Base.metadata.create_all(bind=engine)
```

## Full Example `main.py`

```python
from fastapi import FastAPI
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI with MySQL"}
```

#### What This Line Does

```python
Base.metadata.create_all(bind=engine)
```

SQLAlchemy checks:

```
Does table exist?
```

If not, it creates it automatically.

#### Run the Application

Start server.

```bash
uvicorn app.main:app --reload
```

Now check MySQL:

```sql
SHOW TABLES;
```

Output:

```
users
```

### 📌 3. What is Pydantic Schema?

SQLAlchemy models handle **database structure**.

But FastAPI uses **Pydantic models for request validation**.

So we create **schemas.py**.



#### Step 1: Create `schemas.py`

File:

```
app/schemas.py
```

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
```

This schema validates incoming request data.

Example request:

```json
{
 "name": "Vinod",
 "email": "vinod@gmail.com"
}
```

### Response Schema

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
```

#### Why `orm_mode=True`?

It allows FastAPI to convert SQLAlchemy objects to JSON.

Without it, FastAPI cannot serialize ORM objects.


#### Request Flow

```
Client Request
      ↓
Pydantic Schema Validation
      ↓
SQLAlchemy Model
      ↓
Database
      ↓
Response Schema
      ↓
Client
```

# Real Example

Client sends request:

```json
{
 "name": "Vinod",
 "email": "vinod@gmail.com"
}
```

FastAPI flow:

```
Request → Pydantic Schema → SQLAlchemy Model → Database
```