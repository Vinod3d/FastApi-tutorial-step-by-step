

# 1 Project Folder Structure

Professional backend projects usually follow this structure.

```
fastapi-jwt-app
│
├── app
│   │
│   ├── main.py
│   │
│   ├── config.py
│   │
│   ├── database
│   │   ├── session.py
│   │   └── models.py
│   │
│   ├── schemas
│   │   └── user_schema.py
│   │
│   ├── services
│   │   └── auth_service.py
│   │
│   ├── security
│   │   ├── hashing.py
│   │   ├── jwt_handler.py
│   │   └── oauth2.py
│   │
│   ├── api
│   │   └── auth_routes.py
│   │
│   └── dependencies
│       └── auth_dependency.py
│
└── requirements.txt
```

This structure separates:

* **database**
* **security**
* **business logic**
* **routes**

---

# 2 Install Required Libraries

Install dependencies.

```bash
pip install fastapi uvicorn python-jose passlib[bcrypt] python-multipart
```

Libraries used:

* FastAPI
* python-jose
* Passlib

---

# 3 Create Configuration File

### app/config.py

```python
from pydantic import BaseSettings

class Settings(BaseSettings):

    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
```

This stores:

```
JWT secret
algorithm
token expiry
```

---

# 4 Create Database Model

### app/database/models.py

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class User(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    email: str
    password_hash: str
```

This table stores:

```
id
email
hashed password
```

---

# 5 Create Password Hash Utilities

### app/security/hashing.py

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):

    return pwd_context.verify(password, hashed_password)
```

Purpose:

```
hash password
verify password
```

Example:

```
password → hashed password
```

---

# 6 Create JWT Token Utility

### app/security/jwt_handler.py

```python
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings


def create_access_token(data: dict):

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token
```

Purpose:

```
generate JWT token
```

Token contains:

```
user id
expiry
```

---

# 7 Create OAuth2 Security Scheme

### app/security/oauth2.py

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
```

Meaning:

```
Users login here → /auth/login
```

They receive a **JWT token**.

---

# 8 Create Authentication Service

### app/services/auth_service.py

```python
from sqlmodel import Session, select
from app.database.models import User
from app.security.hashing import verify_password


def authenticate_user(email: str, password: str, session: Session):

    statement = select(User).where(User.email == email)

    user = session.exec(statement).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
```

This function:

```
checks email
verifies password
returns user
```

---

# 9 Create Login Endpoint

### app/api/auth_routes.py

```python
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.security.jwt_handler import create_access_token
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth")


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    token = create_access_token(
        data={"sub": form_data.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

Login request:

```
POST /auth/login
```

Body:

```
username
password
```

Response:

```
access_token
```

---

# 10 Create Protected Route

### app/dependencies/auth_dependency.py

```python
from fastapi import Depends
from jose import jwt

from app.security.oauth2 import oauth2_scheme
from app.config import settings


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    user_email = payload.get("sub")

    return user_email
```

---

### Protected API

```python
from fastapi import Depends

@app.get("/profile")
def get_profile(user = Depends(get_current_user)):

    return {"user": user}
```

This route requires:

```
Authorization header
```

---

# 11 Full Authentication Flow

Step 1

```
User registers
```

Step 2

```
POST /auth/login
```

Body:

```
username
password
```

---

Step 3

Server verifies password and returns:

```
JWT Token
```

Example:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

Step 4

Client sends request:

```
GET /profile
```

Header:

```
Authorization: Bearer TOKEN
```

---

Step 5

Server:

```
decodes token
verifies user
returns response
```

---

# Final Flow Diagram

```
User Login
   ↓
/auth/login
   ↓
Server verifies password
   ↓
JWT Token generated
   ↓
Client stores token
   ↓
Client sends token in header
   ↓
Protected API verifies token
```