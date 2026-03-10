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

# PART 5

# 7. Alembic Migrations

In the previous parts, we created tables using:

```
Base.metadata.create_all()
```

This works for **small projects**, but it is **not used in production systems**.

In real projects we use **Alembic**.

---

# What is Alembic?

Alembic is a **database migration tool for SQLAlchemy**.

It allows developers to:

* track database schema changes
* modify tables safely
* version control database structure

---

## Example Problem Without Alembic

Suppose we initially create a table:

```
users
```

| id | name | email |
| -- | ---- | ----- |

Later we want to add:

```
age column
```

Without migrations we must:

* drop table
* recreate table
* data may be lost

This is **dangerous in production**.

---

## Alembic Solution

Alembic manages database changes safely.

Example migration history:

```
v1 → create users table
v2 → add age column
v3 → add phone column
```

Each change is saved as a **migration file**.

---

# Install Alembic

If not installed earlier:

```bash
pip install alembic
```

---

# Initialize Alembic

Run this command in project root:

```bash
alembic init alembic
```

After running this command, new files are created.

Project structure becomes:

```
fastapi-project
│
├── alembic
│   ├── versions
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
└── app
```

---

## Explanation of Files

| File        | Purpose               |
| ----------- | --------------------- |
| alembic.ini | configuration         |
| env.py      | migration environment |
| versions    | migration history     |

---

# Configure Database URL

Open:

```
alembic.ini
```

Find this line:

```
sqlalchemy.url =
```

Replace with your MySQL connection.

Example:

```
sqlalchemy.url = mysql+pymysql://root:password@localhost:3306/fastapi_db
```

---

# Connect Alembic with Models

Open:

```
alembic/env.py
```

Find this line:

```python
target_metadata = None
```

Replace with:

```python
from app.models import Base
target_metadata = Base.metadata
```

This tells Alembic to **detect SQLAlchemy models**.

---

# Create First Migration

Run:

```bash
alembic revision --autogenerate -m "create users table"
```

Explanation:

| Option       | Meaning              |
| ------------ | -------------------- |
| revision     | create migration     |
| autogenerate | detect model changes |
| -m           | message              |

Alembic creates a file inside:

```
alembic/versions/
```

Example file:

```
f83b2_create_users_table.py
```

---

# Migration File Example

Inside the migration file:

```python
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100)),
        sa.Column('email', sa.String(100))
    )
```

---

# Apply Migration

Run:

```bash
alembic upgrade head
```

This command applies the migration and creates tables.

Database now contains:

```
users table
```

---

# Checking Migration History

Run:

```bash
alembic history
```

Example output:

```
f83b2 -> create users table
```

---

# Updating Database Schema

Suppose we modify our model:

```
add age column
```

Update model:

```python
age = Column(Integer)
```

Now create new migration:

```bash
alembic revision --autogenerate -m "add age column"
```

Then run:

```bash
alembic upgrade head
```

Alembic will update the table **without deleting data**.

---

# Downgrade Migration

If something breaks, we can rollback.

Example:

```
alembic downgrade -1
```

Meaning:

```
go back one migration
```

---

# Migration Workflow

Real development workflow:

```
1 Modify SQLAlchemy model
2 Generate migration
3 Review migration file
4 Apply migration
```

Commands:

```
alembic revision --autogenerate -m "message"
alembic upgrade head
```

---

# Production Importance

Alembic is critical because:

* database schema evolves over time
* teams work together
* deployments require safe schema updates

Without migrations, **production databases can break**.

---

# Interview Questions

### What is Alembic?

Alembic is a **database migration tool for SQLAlchemy** used to manage and track schema changes in a database.

---

### Why are migrations needed?

Migrations allow developers to:

* update database structure
* preserve existing data
* maintain schema version history.

---

### What does `alembic upgrade head` do?

It applies all pending migrations to bring the database to the **latest version**.

---

# Next Part

Next we will learn **Async SQLAlchemy**, which is very important because **FastAPI is asynchronous**.

You will learn:

* async database connection
* async sessions
* async CRUD operations

Reply **“Part 6”** and we will continue.
