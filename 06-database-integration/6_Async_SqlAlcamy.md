Continuing the **FastAPI Database Integration tutorial**.

---

# Chapter 6: Database Integration

| No. | Topic                                                                                                 |
| --- | ----------------------------------------------------------------------------------------------------- |
| 1   | [Introduction to Database Integration in FastAPI](#1-introduction-to-database-integration-in-fastapi) |
| 2   | [What is SQLAlchemy (ORM Concept)](#2-what-is-sqlalchemy-orm-concept)                                 |
| 3   | [Installing and Setting up SQLAlchemy](#3-installing-and-setting-up-sqlalchemy)                       |
| 4   | [Creating Database Connection](#4-creating-database-connection)                                       |
| 5   | [Creating Models in SQLAlchemy](#5-creating-models-in-sqlalchemy)                                     |
| 6   | [CRUD Operations using SQLAlchemy](#6-crud-operations-using-sqlalchemy)                               |
| 7   | [Alembic Migrations](#7-alembic-migrations)                                                           |
| 8   | [Async SQLAlchemy](#8-async-sqlalchemy)                                                               |
| 9   | [Repository Pattern](#9-repository-pattern)                                                           |
| 10  | [Clean Project Structure](#10-clean-project-structure)                                                |

---

# PART 6

# 8. Async SQLAlchemy

FastAPI is built on **ASGI**, which means it supports **asynchronous programming**.

So instead of blocking database operations, we can use **async database queries**.

This improves **performance and scalability**.

---

# Sync vs Async Database

### Synchronous (Traditional)

```text
Request → Wait for DB → Response
```

Server waits until database query finishes.

---

### Asynchronous

```text
Request → Start DB query → handle other requests → return result
```

Server can handle **multiple requests simultaneously**.

---

# Why Async Matters

Suppose:

* 100 users request data
* each DB query takes **1 second**

### Sync server

```text
100 requests → 100 seconds
```

### Async server

```text
100 requests → ~1 second
```

Because queries run concurrently.

---

# Installing Async Dependencies

For MySQL async support we install:

```bash
pip install sqlalchemy
pip install aiomysql
```

Explanation:

| Package    | Purpose            |
| ---------- | ------------------ |
| SQLAlchemy | ORM                |
| aiomysql   | async MySQL driver |

---

# Async Database URL

Async SQLAlchemy uses a slightly different URL.

Example:

```text
mysql+aiomysql://username:password@localhost:3306/fastapi_db
```

---

# Async Database Setup

Create file:

```text
app/database.py
```

---

## Import Async Modules

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
```

---

# Create Async Engine

```python
DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/fastapi_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)
```

Explanation:

| Parameter    | Meaning            |
| ------------ | ------------------ |
| DATABASE_URL | connection string  |
| echo=True    | prints SQL queries |

---

# Create Async Session

```python
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

Explanation:

| Parameter              | Purpose                 |
| ---------------------- | ----------------------- |
| bind                   | connect engine          |
| class_=AsyncSession    | async session           |
| expire_on_commit=False | keeps objects available |

---

# Base Model

```python
Base = declarative_base()
```

---

# Async Database Dependency

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

Explanation:

| Statement  | Meaning                  |
| ---------- | ------------------------ |
| async with | async context manager    |
| yield      | provide session to route |

---

# Example Async CRUD Operation

Create file:

```text
app/crud.py
```

---

## Create User (Async)

```python
from sqlalchemy.future import select

async def create_user(db: AsyncSession, user):

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
```

Notice the use of:

```text
await
```

because operations are asynchronous.

---

# Read Users (Async)

```python
async def get_users(db: AsyncSession):

    result = await db.execute(
        select(User)
    )

    return result.scalars().all()
```

Explanation:

| Function  | Purpose         |
| --------- | --------------- |
| execute() | run query       |
| scalars() | extract objects |
| all()     | return list     |

---

# Async FastAPI Route

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

@router.get("/users")
async def read_users(
    db: AsyncSession = Depends(get_db)
):

    users = await get_users(db)
    return users
```

Notice:

```text
async def
await
```

---

# Async Request Flow

```text
Client Request
      ↓
Async FastAPI Route
      ↓
Async CRUD Function
      ↓
Async SQLAlchemy Query
      ↓
MySQL Database
      ↓
Response
```

---

# Advantages of Async SQLAlchemy

1️⃣ Higher concurrency
2️⃣ Better performance under load
3️⃣ Non-blocking database operations
4️⃣ Scalable APIs

---

# When to Use Async DB

Async is useful when:

* high traffic APIs
* microservices
* many simultaneous requests
* real-time applications

For small apps, sync is often **simpler**.

---

# Sync vs Async Comparison

| Feature        | Sync     | Async        |
| -------------- | -------- | ------------ |
| Complexity     | simple   | more complex |
| Performance    | moderate | high         |
| Concurrency    | limited  | excellent    |
| Learning curve | easy     | harder       |

---

# Interview Questions

### What is Async SQLAlchemy?

Async SQLAlchemy allows database operations to run **asynchronously**, enabling FastAPI to process multiple requests concurrently.

---

### Why do we use `await` with database queries?

Because async database operations return **coroutines**, which must be awaited to get results.

---

### Difference between `Session` and `AsyncSession`?

| Session     | AsyncSession  |
| ----------- | ------------- |
| synchronous | asynchronous  |
| blocking    | non-blocking  |
| simpler     | more scalable |

---

# Next Part

Next we will cover **Repository Pattern**, which is a **very important design pattern used in professional backend systems**.

You will learn:

* clean architecture
* separating database logic
* scalable backend design

Reply **“Part 7”** and we will continue.
