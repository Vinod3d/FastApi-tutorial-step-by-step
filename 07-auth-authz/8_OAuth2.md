Now we move to the **Final Part (Part 8)** of Chapter 7.
This part explains **OAuth2 Scopes**, which provide **fine-grained permission control** in APIs.

---

# Chapter 7: Authentication & Authorization (Part 8)

## OAuth2 Scopes

| No. | Topic                                                               |
| --- | ------------------------------------------------------------------- |
| 1   | [What are OAuth2 Scopes](#1-what-are-oauth2-scopes)                 |
| 2   | [Why Scopes are Used](#2-why-scopes-are-used)                       |
| 3   | [Scopes vs Roles](#3-scopes-vs-roles)                               |
| 4   | [Scopes Example in Real APIs](#4-scopes-example-in-real-apis)       |
| 5   | [Implementing Scopes in FastAPI](#5-implementing-scopes-in-fastapi) |
| 6   | [Creating Scope-Based Security](#6-creating-scope-based-security)   |
| 7   | [Protecting Routes with Scopes](#7-protecting-routes-with-scopes)   |
| 8   | [Interview Questions](#8-interview-questions)                       |

---

# 1. What are OAuth2 Scopes

Scopes define **specific permissions granted to a user or application**.

Instead of giving full access, scopes limit **what actions can be performed**.

Simple idea:

```text
Token → contains scopes
Scopes → define allowed actions
```

Example scopes:

```text
read:user
write:user
delete:user
```

Each scope allows a specific operation.

---

# 2. Why Scopes are Used

Scopes provide **fine-grained access control**.

Without scopes:

```text
User gets full access
```

With scopes:

```text
User gets limited permissions
```

Example:

| Scope       | Permission        |
| ----------- | ----------------- |
| read:user   | read user profile |
| write:user  | update user data  |
| delete:user | remove user       |

---

# 3. Scopes vs Roles

Roles and scopes are related but different.

| Feature | Roles       | Scopes             |
| ------- | ----------- | ------------------ |
| Purpose | Group users | Define permissions |
| Level   | High-level  | Fine-grained       |
| Example | Admin       | read:user          |

Example system:

```text
Role: Admin
Scopes:
- read:user
- write:user
- delete:user
```

---

# 4. Scopes Example in Real APIs

Many popular APIs use scopes.

Example: **GitHub API**

Possible scopes:

```text
repo
user
admin:repo_hook
```

Example: **Google API**

```text
https://www.googleapis.com/auth/drive.readonly
```

Meaning:

```text
Read-only access to Google Drive
```

---

# 5. Implementing Scopes in FastAPI

FastAPI supports OAuth2 scopes through:

```python
OAuth2PasswordBearer
```

Example:

```python
from fastapi.security import OAuth2PasswordBearer
```

---

### Define Scopes

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read:user": "Read user information",
        "write:user": "Update user information"
    }
)
```

This tells FastAPI which scopes exist.

---

# 6. Creating Scope-Based Security

FastAPI provides a class called:

```python
SecurityScopes
```

Example:

```python
from fastapi import Security
from fastapi.security import SecurityScopes
```

---

### Scope Validation Function

```python
def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    token_scopes = payload.get("scopes", [])

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )

    return payload
```

This function checks if the required scope exists.

---

# 7. Protecting Routes with Scopes

Example protected route:

```python
@app.get("/users/me")
def read_user(
    user = Security(
        get_current_user,
        scopes=["read:user"]
    )
):
    return user
```

This route requires:

```text
read:user scope
```

---

### Example Token Payload

```json
{
 "sub": "vinod",
 "scopes": ["read:user", "write:user"]
}
```

This user can:

* read user data
* update user data

But cannot:

```text
delete users
```

---

### Request Example

```text
GET /users/me
Authorization: Bearer <token>
```

If token lacks required scope:

```json
{
 "detail": "Not enough permissions"
}
```

---

# 8. Interview Questions

### What are OAuth2 scopes?

OAuth2 scopes define specific permissions that an access token grants to a client.

---

### Why are scopes used?

Scopes restrict access to specific resources or actions, improving API security.

---

### What is the difference between roles and scopes?

Roles represent user categories, while scopes represent individual permissions.

---

### How are scopes implemented in FastAPI?

Scopes are implemented using **OAuth2PasswordBearer**, **SecurityScopes**, and dependency functions to validate required permissions.

---

# Final Summary of Chapter 7

Authentication system includes:

```text
Password hashing
OAuth2 authentication
JWT tokens
Token expiration
Refresh tokens
RBAC
Scopes
```

Authentication flow:

```text
User login
   |
   v
Server verifies credentials
   |
   v
Server creates JWT token
   |
   v
Client sends token with requests
   |
   v
Server verifies token and permissions
```

---

# You Have Completed Chapter 7 🎉

Topics covered:

| Topic                           | Status |
| ------------------------------- | ------ |
| Authentication vs Authorization | ✅      |
| JWT                             | ✅      |
| Password hashing                | ✅      |
| OAuth2 password flow            | ✅      |
| Token expiration                | ✅      |
| Refresh tokens                  | ✅      |
| RBAC                            | ✅      |
| Scopes                          | ✅      |

---

If you want, I can also give you a **Production-Level FastAPI Authentication Architecture** that companies use (with folders like **routers, services, dependencies, schemas, security**).
It will make your **FastAPI repo look like a professional backend project**, which is very useful for **GitHub and job interviews**.
