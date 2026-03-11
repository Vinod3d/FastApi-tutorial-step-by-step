
# 1. What is Password Hashing

Password hashing is the process of **converting a password into a secure fixed-length string** using a hashing algorithm.

Example:

```id="m12b4c"
password: mypassword123
```

After hashing:

```id="u45q9f"
$2b$12$9M0vZC2l...
```

This hashed value is stored in the database.

---

### Important Point

> We never store plain passwords in databases.

Instead we store **hashed passwords**.

---

# 2. Why Password Hashing is Important

If passwords are stored in plain text:

```id="j67p2v"
users table

id | username | password
1  | vinod    | 123456
```

If database leaks → all passwords exposed.

---

With hashing:

```id="g11q7k"
users table

id | username | password
1  | vinod    | $2b$12$3fdksdfl...
```

Even if database leaks → attacker cannot easily recover passwords.

---

# 3. Hashing vs Encryption

Many beginners confuse these.

| Feature    | Hashing                 | Encryption               |
| ---------- | ----------------------- | ------------------------ |
| Purpose    | Secure password storage | Secure data transmission |
| Reversible | No                      | Yes                      |
| Example    | bcrypt                  | AES                      |

Example:

Hashing:

```id="g2p6xb"
password → hash
```

Encryption:

```id="g1s5kz"
data → encrypted → decrypted
```

---

# 4. Password Hashing in FastAPI

FastAPI commonly uses:

```id="9xwzfe"
passlib
bcrypt
```

These libraries securely hash passwords.

---

### Why bcrypt?

Because bcrypt:

* adds **salt**
* prevents **rainbow table attacks**
* slows down brute force attacks

---

# 5. Installing Required Libraries

Install dependencies:

```bash
pip install passlib[bcrypt]
```

Also install JWT library:

```bash
pip install python-jose
```

---

# 6. Creating Password Hash Functions

Example hashing code:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
```

---

### Function to Hash Password

```python
def hash_password(password: str):
    return pwd_context.hash(password)
```

Example:

```python
hash_password("mypassword123")
```

Output:

```id="u71t8x"
$2b$12$hF93kdjf9...
```

---

### Function to Verify Password

```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
```

Example:

```python
verify_password(
    "mypassword123",
    stored_hash
)
```

Returns:

```id="p88r3z"
True
```

---

# 7. What is OAuth2 Password Flow

OAuth2 is an **authorization framework** used for secure login.

FastAPI supports many OAuth2 flows.

Most common:

```id="c18p4v"
OAuth2 Password Flow
```

---

### What OAuth2 Password Flow Means

User sends:

```id="e31y7q"
username + password
```

Server verifies credentials.

If correct:

```id="h73x5b"
Server returns access token
```

Client uses this token for future requests.

---

# 8. OAuth2 Authentication Flow

Step-by-step process:

### Step 1 Login Request

```id="h0b7f2"
POST /token
```

Request:

```id="q41h3s"
username=vinod
password=123456
```

---

### Step 2 Server Validates Credentials

Server checks database.

---

### Step 3 Token Generated

Server creates:

```id="r98x4y"
JWT token
```

---

### Step 4 Client Sends Token

Future requests:

```id="t63v9a"
Authorization: Bearer <token>
```

---

# 9. FastAPI OAuth2 Implementation

FastAPI provides a built-in class:

```python
from fastapi.security import OAuth2PasswordBearer
```

---

### Creating OAuth2 Scheme

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)
```

This means:

```id="k33v1t"
Client must send token from /token endpoint
```

---

### Using OAuth2 Dependency

Example protected route:

```python
from fastapi import Depends

@app.get("/profile")
def read_profile(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Here:

```id="z53g7u"
Depends(oauth2_scheme)
```

Extracts the **JWT token** from request header.

---

### Request Example

Client sends request:

```id="f60p5y"
GET /profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

FastAPI automatically extracts token.

---

# 10. Interview Questions

### What is password hashing?

Password hashing converts a password into a secure fixed-length string so that the original password cannot be retrieved.

---

### Why do we hash passwords?

Passwords are hashed to prevent exposure if the database is compromised.

---

### Which libraries are used for password hashing in FastAPI?

Common libraries:

* passlib
* bcrypt

---

### What is OAuth2 Password Flow?

OAuth2 password flow allows users to authenticate by sending their username and password to obtain an access token.

---

# Summary

Password storage:

```id="a19v0k"
password → hash → store in DB
```

OAuth2 flow:

```id="u08f2q"
Login → Verify → Generate Token → Access API
```

---

# Next Part (Part 4)

Next we will build **complete JWT authentication in FastAPI**:

* Create JWT tokens
* Token expiration
* Login endpoint
* Protected routes
* Token verification
* Full working FastAPI authentication system

This will be the **most practical coding part**.
