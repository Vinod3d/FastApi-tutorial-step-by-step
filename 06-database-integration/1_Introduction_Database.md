# Database Integration in FastAPI

When we build an API, we usually need to **store data permanently**.

Example:

User registers → data saved in database
User logs in → data fetched from database
Orders → stored in database

Without a database, data will disappear when the server stops.

#### Example Flow

```
Client → FastAPI → Database
```

Example request:

```
POST /users
```

FastAPI will:

1. Receive request
2. Validate data using Pydantic
3. Store data in database
4. Return response


### 📌 What is SQLAlcamy

**SQLAlchemy** is a popular **Python library used for working with relational databases**. It acts as a bridge between a Python application and a database.

It provides an **ORM (Object Relational Mapper)** that allows developers to interact with database tables using **Python classes and objects instead of writing raw SQL queries**.

SQLAlchemy supports many databases such as **MySQL, PostgreSQL, SQLite, Oracle, and SQL Server**. It also provides two main components: **SQLAlchemy Core** for writing SQL expressions and **SQLAlchemy ORM** for mapping database tables to Python classes.

**In short:**
SQLAlchemy is a powerful Python toolkit and ORM that simplifies database operations by allowing developers to manage databases using Python code instead of direct SQL queries.



### 📌 Why SQLAlchemy is Used in FastAPI

SQLAlchemy is used in FastAPI to manage database operations efficiently. It provides ORM functionality that allows developers to interact with databases using Python objects instead of raw SQL queries, making the code cleaner, more maintainable, and database-independent.

#### Without ORM (Raw SQL)

Example:

```sql
INSERT INTO users (name, email)
VALUES ('Vinod', 'vinod@gmail.com');
```

#### With ORM

Example:

```python
user = User(name="Vinod", email="vinod@gmail.com")
db.add(user)
db.commit()
```

ORM makes database code **clean and Pythonic**.

### 📌 Advantages of Using SQLAlchemy

1️⃣ Works with many databases
2️⃣ Clean Python syntax
3️⃣ Handles relationships
4️⃣ Supports async operations
5️⃣ Very powerful query system



## Interview Questions

### Q1: What is ORM?

ORM (Object Relational Mapping) is a technique that allows developers to interact with databases using **programming language objects instead of SQL queries**.

Example:

```
User(name="Vinod")
```

instead of

```
INSERT INTO users...
```

### Q2: Why use SQLAlchemy with FastAPI?

Because FastAPI does not include built-in database support, SQLAlchemy is used to:

* manage database connections
* map Python objects to database tables
* perform CRUD operations easily.

### Q3: What databases work with SQLAlchemy?

Examples:

* PostgreSQL
* MySQL
* SQLite
* MariaDB
* Oracle

## Real Production Stack

Most FastAPI production apps use:

```
FastAPI
SQLAlchemy
Alembic
PostgreSQL
```

