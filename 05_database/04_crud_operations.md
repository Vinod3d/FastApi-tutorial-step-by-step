# CRUD Operations (Create, Read, Update, Delete)

## What you will learn
- Performing standard CRUD logic with SQLAlchemy
- Properly injecting the Database Session (`Depends(get_db)`)
- Using `db.commit()` and `db.refresh()`
- Separating your CRUD operations from your router logic safely

## Concept (Simple Explanation)
**CRUD** stands for **C**reate, **R**ead, **U**pdate, and **D**elete. These are the four basic functions almost every application needs.
Think of the database as a giant filing cabinet.
- **Create:** Filling out a new folder and sliding it in.
- **Read:** Opening the cabinet to look at a folder.
- **Update:** Erasing a line on an existing document and writing something new.
- **Delete:** Shredding the folder entirely.

## Code Example
**`crud.py` (The Database Logic)**
```python
from sqlalchemy.orm import Session
import models, schemas

# CREATE
def create_user(db: Session, user: schemas.UserCreate):
    # 1. Convert Pydantic Schema to SQLAlchemy Model
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)      # 2. Stage the object
    db.commit()          # 3. Save it to the database permanently
    db.refresh(db_user)  # 4. Reload it to get the auto-generated ID!
    return db_user

# READ
def get_user(db: Session, user_id: int):
    # Retrieve the first user matching the ID
    return db.query(models.User).filter(models.User.id == user_id).first()

# UPDATE
def update_user(db: Session, user_id: int, updated_data: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    # Modify the object
    db_user.name = updated_data.name
    db_user.email = updated_data.email
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
```

## Best Practices
- **Isolate CRUD logic:** Look at the example above—none of those functions mention `FastAPI`, `APIRouter`, or `HTTPException`. They purely handle data. When building routers, import these functions. This makes your application massively easier to unit test.

## Common Mistakes
- **Forgetting `db.commit()`:** Calling `db.add()` places the object in staging memory. If you forget to commit, the changes will vanish when the request ends.
- **Forgetting `db.refresh()`:** If you create an item, the database assigns its primary key (ID). If you don't call `refresh` after committing, your Python object will have `id = None` and your API response will be broken!

## Interview Questions
**Q: Explain the flow of an incoming `POST` request all the way to the Database.**
A: 
1. The Client sends an HTTP Request containing a JSON Body.
2. The FastAPI Route intercepts it, and Pydantic maps/validates the JSON into a Schema.
3. The Route passes the Pydantic object and the `db` Session to the CRUD layer.
4. The CRUD layer maps the Pydantic data into a SQLAlchemy Model, adds it to the session, and Commits it.
5. The Database executes the SQL `INSERT` statement and returns success.

**Q: In SQLAlchemy, what is the difference between `.first()` and `.all()`?**
A: `.all()` returns a list containing every single row that matched the query. `.first()` returns only the very first underlying object found, or `None` if the query matched nothing, stopping the database search immediately for high performance.
