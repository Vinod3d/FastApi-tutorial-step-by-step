# SQLAlchemy (Synchronous) Setup

## What you will learn
- Setting up a MySQL/PostgreSQL connection using SQLAlchemy
- The role of the `Engine`, `SessionLocal`, and `Base` class
- Defining your first Database Model (Table structure)
- The difference between ORM Models and Pydantic Schemas

## Concept (Simple Explanation)
Python doesn't naturally speak SQL. If you want to save a `User` object to a database, you need a translator. **SQLAlchemy** is that translator (an Object Relational Mapper or ORM). 
It takes your regular Python classes and automatically generates the complex SQL (`INSERT INTO users...`) needed to talk to MySQL or PostgreSQL. 

- **Engine:** The physical engine that connects to the database.
- **SessionLocal:** A temporary "conversation" your app has with the database.
- **Base:** The parent class that tells SQLAlchemy "Translate any class that inherits from me into a database table."

## Code Example
**1. Connection Setup (`database.py`)**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL Example (requires pip install pymysql)
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/fastapi_db"

# 1. Create the Engine (The Connection)
engine = create_engine(DATABASE_URL, echo=True)

# 2. Create a Session Factory 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base Class
Base = declarative_base()
```

**2. Defining a Model (`models.py`)**
```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
```

## Best Practices
- **Never hardcode database URLs:** Always load the `DATABASE_URL` from environment variables using `python-dotenv` or Pydantic `BaseSettings`. Exposing credentials in Github is a catastrophic security risk.
- **Use `echo=True` only in development:** While it is great for seeing exactly what SQL queries are running under the hood, it slows down production servers and litters logs.

## Common Mistakes
- **Confusing SQLAlchemy Models with Pydantic Models:** 
  - *SQLAlchemy Model (`models.User`):* Talks to the Database. Uses `= Column(String)`.
  - *Pydantic Model (`schemas.User`):* Talks to the Client/Internet. Uses `: str`.
  *Do not mix them up!*

## Interview Questions
**Q: What is a SQLAlchemy Engine?**
A: The Engine is the starting point for any SQLAlchemy application. It is the core object that manages the connection pool and acts as the interface to execute SQL queries against the database dialect (like MySQL or Postgres).

**Q: Why do we use `autocommit=False` when creating a session?**
A: If autocommit is true, every single database query automatically saves permanently. By setting it to false, we can group multiple queries into a single "Transaction" and manually call `db.commit()`. If one query fails, we can `db.rollback()` safely.
