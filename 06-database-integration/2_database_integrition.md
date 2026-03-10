

# Installing and Setting up SQLAlchemy for MySQL

When we use **MySQL with FastAPI**, we need a **database driver** that allows Python to communicate with MySQL.

### 📌 1. Install Required Packages

```bash
pip install sqlalchemy
pip install pymysql
pip install alembic
```

Explanation:

| Package    | Purpose                     |
| ---------- | --------------------------- |
| SQLAlchemy | ORM for database operations |
| PyMySQL    | MySQL driver                |
| Alembic    | Database migration tool     |



### 📌 2. Clean Project Structure

In real FastAPI applications, database-related files are organized separately.

Example structure:

```
fastapi-project
│
├── app
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers
│       └── users.py
│
└── requirements.txt
```

### Explanation

| File        | Role                              |
| ----------- | --------------------------------- |
| main.py     | FastAPI entry point               |
| database.py | Database connection configuration |
| models.py   | SQLAlchemy table models           |
| schemas.py  | Pydantic validation schemas       |
| crud.py     | Database query logic              |
| routers     | API endpoints                     |

This structure keeps the project **clean and scalable**.

### 📌 3. Creating Database Connection

Now we connect FastAPI with **MySQL database**.

#### Step 1: Create MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE fastapi_db;
```

Now we have a database called:

```
fastapi_db
```

#### Step 2: Create `database.py`

Create a file:

```
app/database.py
```

Import required modules:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
```

#### Step 3: MySQL Database URL

SQLAlchemy database URL format:

```
mysql+pymysql://username:password@host:port/database_name
```

Example:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/fastapi_db"
```

Explanation:

| Part       | Meaning        |
| ---------- | -------------- |
| mysql      | Database type  |
| pymysql    | Driver         |
| root       | MySQL username |
| password   | MySQL password |
| localhost  | Database host  |
| 3306       | MySQL port     |
| fastapi_db | Database name  |

---

#### Step 4: Create Engine

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
```

### What is `echo=True`?

It prints SQL queries in terminal.

Example output:

```
SELECT * FROM users
```

This helps during debugging.


#### Step 5: Create Session

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

### What is Session?

Session represents a **temporary connection to the database** used for executing queries.

Example operations:

* Insert data
* Fetch data
* Update records
* Delete records

#### Step 6: Base Class for Models

```python
Base = declarative_base()
```

All SQLAlchemy models will inherit from this base class.

Example:

```python
class User(Base):
```

#### Final `database.py` (MySQL Version)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/fastapi_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```


# Dependency Injection for Database Session

FastAPI uses dependency injection to provide database sessions to routes.

Add this function in `database.py`.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Why `yield` is Used?

`yield` allows FastAPI to:

1. create database session
2. provide it to API route
3. automatically close session after request

This prevents **database connection leaks**.

### Using Database Session in FastAPI Route

Example:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return {"message": "DB connected"}
```

Explanation:

```
Depends(get_db)
```

FastAPI automatically injects the **database session**.


### Database Request Lifecycle

```
Client Request
       ↓
FastAPI Route
       ↓
Dependency (get_db)
       ↓
Session Created
       ↓
Query Executed
       ↓
Session Closed
```

# Interview Questions

### Q1: What is SQLAlchemy Engine?

Engine is the **core component that manages database connections and executes SQL queries**.


### Q2: What is sessionmaker?

`sessionmaker` is a factory that creates **new database sessions**.

Example:

```
SessionLocal()
```

creates a new session.

### Q3: Why do we close DB session?

Closing the session prevents:

* memory leaks
* connection pool exhaustion
* database performance issues

### Real Production Stack

Most production FastAPI applications use:

```
FastAPI
SQLAlchemy
Alembic
MySQL / PostgreSQL
```
