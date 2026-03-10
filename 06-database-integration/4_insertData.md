## CRUD Operations using SQLAlchemy


#### Step 1: Create CRUD File

Create a file:

```
app/crud.py
```

Import dependencies.

```python
from sqlalchemy.orm import Session
from . import models, schemas
```

### CREATE Operation

This function inserts a new user into the database.

```python
def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
```


## Explanation

### Creating Object

```python
new_user = models.User(...)
```

This creates a **Python object representing a database row**.


### Adding to Session

```python
db.add(new_user)
```

Adds object to database session.

### Saving Data

```python
db.commit()
```

Executes SQL query and saves data permanently.

Equivalent SQL:

```sql
INSERT INTO users (name, email)
VALUES ('Vinod','vinod@gmail.com');
```

### Refresh Object

```python
db.refresh(new_user)
```

Reloads object from database so we get generated values like:

```
id
```

### READ Operation (Get All Users)

```python
def get_users(db: Session):
    return db.query(models.User).all()
```

Equivalent SQL:

```sql
SELECT * FROM users;
```

### READ Operation (Get Single User)

```python
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
```

Equivalent SQL:

```sql
SELECT * FROM users WHERE id = 1;
```

### UPDATE Operation

```python
def update_user(db: Session, user_id: int, user: schemas.UserCreate):

    existing_user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not existing_user:
        return None

    existing_user.name = user.name
    existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)

    return existing_user
```

Equivalent SQL:

```sql
UPDATE users
SET name='Rahul', email='rahul@gmail.com'
WHERE id=1;
```

### DELETE Operation

```python
def delete_user(db: Session, user_id: int):

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user
```

Equivalent SQL:

```sql
DELETE FROM users WHERE id=1;
```

#### Step 2: Create API Routes

Create file:

```
app/routers/users.py
```

Import dependencies.

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud
```


# Create Router

```python
router = APIRouter(prefix="/users", tags=["Users"])
```

---

# Create User API

```python
@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
```

---

# Get All Users

```python
@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)
```

---

# Get Single User

```python
@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):

    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

---

# Update User

```python
@router.put("/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

    updated_user = crud.update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user
```

---

# Delete User

```python
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    deleted_user = crud.delete_user(db, user_id)

    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}
```

---

# Step 3: Register Router in main.py

Open **main.py**.

```python
from fastapi import FastAPI
from app.routers import users

app = FastAPI()

app.include_router(users.router)
```

---

# Test API

Run server:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Available endpoints:

| Method | Endpoint    | Purpose       |
| ------ | ----------- | ------------- |
| POST   | /users      | Create user   |
| GET    | /users      | Get all users |
| GET    | /users/{id} | Get user      |
| PUT    | /users/{id} | Update user   |
| DELETE | /users/{id} | Delete user   |

---

# Complete Request Flow

```
Client Request
      ↓
FastAPI Route
      ↓
Pydantic Schema Validation
      ↓
CRUD Layer
      ↓
SQLAlchemy Model
      ↓
MySQL Database
      ↓
Response
```

---

# Interview Questions

### What is CRUD?

CRUD stands for:

Create, Read, Update, Delete — the four basic operations performed on database records.

---

### Why use a separate CRUD layer?

Advantages:

* cleaner code
* reusable logic
* easier testing
* separation of concerns

---

### What does `db.refresh()` do?

It reloads the object from the database to get updated values such as **auto-generated ID**.
