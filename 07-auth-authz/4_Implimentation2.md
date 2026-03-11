

# 1. Required Libraries for JWT Authentication

Install required libraries.

```bash
pip install python-jose passlib[bcrypt]
```

Libraries used:

| Library     | Purpose                             |
| ----------- | ----------------------------------- |
| python-jose | JWT token creation and verification |
| passlib     | Password hashing                    |
| bcrypt      | Secure hashing algorithm            |

---

# 2. Project Structure for Authentication

A simple FastAPI authentication project can look like this:

```id="x2a1t"
app/
 ├── main.py
 ├── auth.py
 ├── models.py
 ├── database.py
 └── utils.py
```

For learning purposes we will implement everything inside **main.py**.

---

# 3. Creating Password Hashing Functions

First create hashing utilities.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

---

### Hash Password Function

```python
def hash_password(password: str):
    return pwd_context.hash(password)
```

Example:

```id="l7d8c"
hash_password("mypassword")
```

Output will be a **hashed password**.

---

### Verify Password Function

```python
def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

This checks if the password entered by the user matches the stored hash.

---

# 4. Creating JWT Token Function

Now we create a function to generate JWT tokens.

```python
from jose import jwt
from datetime import datetime, timedelta
```

Secret key configuration:

```python
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

### Token Creation Function

```python
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
```

Example token payload:

```json id="j7x2n"
{
 "sub": "vinod",
 "exp": "expiration time"
}
```

---

# 5. Creating Fake Database for Example

For tutorial purposes we use a fake database.

```python
fake_users_db = {
    "vinod": {
        "username": "vinod",
        "hashed_password": hash_password("123456")
    }
}
```

---

# 6. Login Endpoint to Generate Token

FastAPI provides a class for login forms.

```python
from fastapi.security import OAuth2PasswordRequestForm
```

---

### Login Route

```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_users_db.get(
        form_data.username
    )

    if not user:
        return {"error": "User not found"}

    if not verify_password(
        form_data.password,
        user["hashed_password"]
    ):
        return {"error": "Incorrect password"}

    access_token = create_access_token(
        data={"sub": user["username"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

---

### Login Request Example

Request:

```id="r4g1v"
POST /token
```

Body (form data):

```id="a9b8c"
username=vinod
password=123456
```

Response:

```json id="p3t2k"
{
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
 "token_type": "bearer"
}
```

---

# 7. Creating Dependency to Get Current User

Now we extract the token from requests.

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)
```

---

### Get Current User Function

```python
from jose import JWTError

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise Exception("Invalid token")

        return username

    except JWTError:
        raise Exception("Token validation failed")
```

---

# 8. Creating Protected Routes

Now we secure endpoints.

Example:

```python
@app.get("/profile")
def read_profile(
    user: str = Depends(get_current_user)
):
    return {
        "message": f"Welcome {user}"
    }
```

---

### Protected Request Example

Request:

```id="c4b7p"
GET /profile
Authorization: Bearer <token>
```

Response:

```json id="k1q3y"
{
 "message": "Welcome vinod"
}
```

---

# 9. Complete Working Example

Flow of authentication system:

```id="j9z4s"
User login
     |
     v
POST /token
     |
     v
Server verifies credentials
     |
     v
Server generates JWT token
     |
     v
Client sends token in requests
     |
     v
Protected API validates token
     |
     v
Access granted
```

---

# 10. Interview Questions

### What library is used to create JWT in FastAPI?

Common libraries include:

* python-jose
* PyJWT

---

### What does OAuth2PasswordRequestForm do?

It extracts **username and password from login requests**.

---

### What does OAuth2PasswordBearer do?

It extracts the **JWT token from Authorization headers**.

---

### What is the "sub" field in JWT?

"sub" stands for **subject** and usually contains the user identifier.

---

# Summary

Login system:

```id="c5x8y"
User login → Generate JWT → Access protected APIs
```

Security layers used:

```id="d9e2h"
Password hashing
JWT tokens
OAuth2 authentication
Protected routes
```

---

# Next Part (Part 5)

Next we will cover **Token Expiration**:

* Why tokens expire
* How expiration works
* Security benefits
* Handling expired tokens
* FastAPI expiration implementation

This is **important for real production APIs**.
