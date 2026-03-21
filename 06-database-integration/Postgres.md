### Postgres

Postgres Credential

```
Username: postgres
Password: 1234
```
CMD Commond

```
psql -U postgres

```

## `database.py`

```python
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import settings

# Async PostgreSQL engine
engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)

# Async session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_tables() -> None:
    from .models import Shipment  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


# Session dependency annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

## `config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
```

## `.env` file

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_PORT=5432
POSTGRES_DB=fastship
```

## Required package

Async PostgreSQL ke liye ye install hona chahiye:

```bash
pip install asyncpg sqlmodel
```

Agar pehle se nahi hai to:

```bash
pip install fastapi sqlalchemy pydantic-settings
```

---

## `main.py` 

```python
from fastapi import FastAPI
from app.database import create_db_tables

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_tables()


@app.get("/")
async def home():
    return {"message": "Database connected successfully"}
```

## Important

Agar tum async setup use kar rahe ho, to route me bhi DB queries `await` ke saath karni padengi.

Example:

```python
from sqlmodel import select

@app.get("/shipments")
async def get_shipments(session: SessionDep):
    result = await session.execute(select(Shipment))
    shipments = result.scalars().all()
    return shipments
```