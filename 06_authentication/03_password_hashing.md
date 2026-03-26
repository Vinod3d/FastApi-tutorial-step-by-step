# Password Hashing & OAuth2 Flow

## What you will learn
- Why storing plain-text passwords is a catastrophic failure
- The difference between Hashing and Encryption
- Implementing `passlib` and `bcrypt` in FastAPI
- Setting up the OAuth2 Password Bearer flow

## Concept (Simple Explanation)
If you store User passwords like `"password123"` in your database, a single database leak ruins the lives of thousands of users (who inevitably reuse that password for their bank). 

You must **Hash** the password. 
- **Encryption:** Like translating English to Morse Code. You can translate it back. (Reversible).
- **Hashing:** Like putting an apple in a blender. You get apple juice. You can *never* put the apple back together. (Irreversible).

When a user registers, you blend their password into a hash (`$2b$12$9M...`) and save the hash. When they log in, they type their password. You blend it again. If the two glasses of juice look identical, the password is correct! You never actually know what their password is.

## Installation
To use `passlib` with the `bcrypt` hashing algorithm in FastAPI, install it using pip:

```bash
pip install "passlib[bcrypt]"
```

## Code Example
**1. Password Hashing Logic (`security.py`)**
```python
from passlib.context import CryptContext

# Define bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Converts "password123" into an irreversible string
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Safely compares the plain text input against the stored hash
    return pwd_context.verify(plain_password, hashed_password)
```

**2. OAuth2 In FastAPI (`main.py`)**
FastAPI has built-in support for Swagger UI login via `OAuth2PasswordBearer`.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# Tells FastAPI where the login URL is located
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real app, you fetch the user from the DB and verify_password() here
    if form_data.username == "vinod" and form_data.password == "secret":
        return {"access_token": "fake_jwt_token", "token_type": "bearer"}
    
    raise HTTPException(status_code=400, detail="Incorrect username or password")

# Adding the dependency forces a lock icon on Swagger UI!
@app.get("/secure-data")
def read_secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "You provided a token!", "token": token}
```

## Best Practices
- **Use `bcrypt` or `Argon2`:** These algorithms are specifically designed to be *slow*. If a hacker steals your database, they will try to "brute-force" guess passwords by hashing millions of strings a second. Bcrypt intentionally takes ~0.3 seconds per hash to ruin their processing speed.

## Common Mistakes
- **Using MD5 or SHA-256 for passwords:** These are fast cryptographic hashes meant for verifying file downloads. They can be cracked billions of times a second. They are completely insecure for passwords.

## Interview Questions
**Q: What is a "Salt" in password hashing?**
A: A salt is a random string automatically appended to a password before hashing. If two users have the exact same password ("admin123"), without a salt, their hashes would look identical in the database. A unique salt ensures their final hashes look completely different, neutralizing attacks like "Rainbow Tables."

**Q: Explain the OAuth2 Password Flow in FastAPI.**
A: The client sends a `POST` request containing `username` and `password` as form-data to the `tokenUrl`. The server verifies these credentials against the database. If correct, the server issues a standard JSON response containing an `access_token` and `token_type` (usually "bearer"). The client includes this token in the `Authorization` header for future requests.
