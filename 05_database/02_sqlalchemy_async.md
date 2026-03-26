# Async SQLAlchemy

## What you will learn
- The difference between Sync and Async database execution
- Configuring an Async Engine and Async Session
- Using `await` securely with database transactions

## Concept (Simple Explanation)
Imagine a restaurant with one waiter (Synchronous). If a customer asks for a 20-minute steak (a heavy database query), the waiter stands at their table for 20 minutes doing nothing while other tables get angry.

**Async SQLAlchemy** turns the waiter asynchronous. They put the steak order in the kitchen (the database) and *immediately* go serve 50 other tables. When the steak is finally ready, they pick it up and deliver it.

Because FastAPI is an inherently asynchronous framework, utilizing Async SQLAlchemy allows your server to handle thousands of simultaneous requests without blocking on database I/O.

## Code Example
**Async Connection Setup (`database.py`)**
```python
# Notice we import from the .asyncio library now!
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Use an async driver (aiomysql for MySQL, asyncpg for Postgres)
DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/fastapi_db"

# 2. Use create_async_engine
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. Use AsyncSession for the class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# 4. Async Dependency Generator
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## Best Practices
- **Use `asyncpg` or `aiomysql`:** To do async operations, the underlying driver must be async. Standard `psycopg2` or `pymysql` block the thread.
- **Set `expire_on_commit=False`:** In async sessions, you cannot easily access attributes of a database object after you log off the session if it's expired. Setting this to false prevents "detached instance" errors after calling `await db.commit()`.

## Common Mistakes
- **Forgetting `await`:** When using async SQLAlchemy, running `db.execute(...)` returns a coroutine initially, not the data. You absolutely must run `result = await db.execute(...)`.
- **Using `.first()` or `.all()` directly on a query:** In modern Async SQLAlchemy 2.0, you don't do `db.query(User).all()`. Instead, you use `await db.execute(select(User))`, and then extract the data via `.scalars().all()`.

## Interview Questions
**Q: When should you explicitly use Async SQLAlchemy over Synchronous SQLAlchemy?**
A: Async is highly beneficial for high-traffic APIs or microservices where the server handles hundreds/thousands of concurrent requests heavily bounded by Database I/O interactions. For small, low-traffic internal tools, standard sync SQLAlchemy might be easier and completely sufficient.

**Q: What does `result.scalars().all()` do in an async database operation?**
A: When you execute an async SQL `select()` statement, SQLAlchemy returns a "Result" object holding rows (like tuples). Calling `.scalars()` extracts the first column of those rows (which is your actual ORM Object), and `.all()` returns them as a clean Python list.
