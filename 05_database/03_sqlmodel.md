# SQLModel Overview

## What you will learn
- What SQLModel is and why it exists
- Combining Pydantic and SQLAlchemy into one class
- Drastically reducing code duplication in modern FastAPI projects

## Concept (Simple Explanation)
In standard FastAPI, you suffer from "Definition Fatigue". 
1. You write a `Model` in SQLAlchemy to create the database table.
2. You write a nearly identical `Schema` in Pydantic to validate the client's API request.

**SQLModel** (created by the author of FastAPI, Sebastián Ramírez) merges them. Think of it as a hybrid car that uses both gas and electric dynamically. You write **one** class, and SQLModel treats it as a Pydantic model when validating API requests, and as an SQLAlchemy model when talking to the database!

## Code Example
```python
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends

# 1. ONE Class to rule them all! 
# Inherits from SQLModel, acts as both Table AND Validation Schema
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = None

# Database Setup
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

# 2. We use the SAME class 'Hero' for the request body type!
@app.post("/heroes/")
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    # 3. And we use the exact same object to save to the database!
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

## Best Practices
- **Use Multiple Models for Data Hiding:** Even with SQLModel, you shouldn't return passwords to clients. Write a base class `HeroBase(SQLModel)` containing shared fields, then inherit from it to create `HeroCreate` (with password) and `HeroPublic` (without password).
- **Embrace Type Annotations:** SQLModel leverages modern Python 3.10+ typing beautifully (`id: int | None`). Learn modern type-hinting to get the most out of it.

## Common Mistakes
- **Forgetting `table=True`:** If you just write `class Hero(SQLModel):`, it acts purely as a Pydantic validation model. You *must* add `table=True` for SQLModel to actually generate a database table for it!

## Interview Questions
**Q: What specific problem does SQLModel solve in the FastAPI ecosystem?**
A: It solves code replication. Traditionally, developers have to maintain one SQLAlchemy class for the data layer and one Pydantic class for the web layer, which often look 95% identical. SQLModel unifies them into a single definition framework.

**Q: Is SQLModel a brand new ORM from scratch?**
A: No. Underneath the hood, it is highly optimized "glue" that perfectly combines SQLAlchemy Core/ORM with Pydantic. It uses SQLAlchemy's robust database engine and Pydantic's state-of-the-art validation.
