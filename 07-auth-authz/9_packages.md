

## 1. `passlib[argon2]`

**Passlib** is a Python library used for **password hashing**.

It helps store passwords securely in databases.

`argon2` is a **modern and very secure hashing algorithm**.

Example:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

hashed = pwd_context.hash("mypassword")
```

Use case:

* Hash user passwords
* Verify passwords during login

Example systems using password hashing:

* Login systems
* Authentication APIs
* User registration systems


## 2. `python-jose[cryptography]`

`python-jose` is a library used to **create and verify JWT tokens**.

JWT is used for **authentication in APIs**.

Example:

```python
from jose import jwt

token = jwt.encode({"user_id": 1}, "secret", algorithm="HS256")
```

Use case:

* Generate access tokens
* Decode tokens
* Authenticate API users

Commonly used with:

* FastAPI
* Django REST
* Flask APIs

## 3. `python-multipart`

This library is used to **handle form data and file uploads**.

FastAPI needs this when receiving:

* form data
* file uploads
* login forms

Example:

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

Without this library, FastAPI cannot process:

```
multipart/form-data
```

## 4. `pydantic[email]`

`pydantic` is used in FastAPI for **data validation**.

The `[email]` extra installs a library that allows **email validation**.

Example:

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
```

Example valid input:

```
test@gmail.com
```

Example invalid input:

```
testgmail.com
```

FastAPI will automatically return a validation error.

## Summary

| Library                   | Purpose                            |
| ------------------------- | ---------------------------------- |
| passlib[argon2]           | Password hashing                   |
| python-jose[cryptography] | JWT authentication                 |
| python-multipart          | Form data and file upload handling |
| pydantic[email]           | Email validation                   |


These libraries are commonly installed together when building a **FastAPI authentication system**.

Example install command:

```bash
pip install passlib[argon2] python-jose[cryptography] python-multipart pydantic[email]
```