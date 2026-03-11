Now we move to **Part 6** of Chapter 7.
This part explains **Refresh Tokens**, which are used in **real production authentication systems** like Google, GitHub, and many SaaS platforms.

---

# Chapter 7: Authentication & Authorization (Part 6)

## Refresh Tokens

| No. | Topic                                                                               |
| --- | ----------------------------------------------------------------------------------- |
| 1   | [What is a Refresh Token](#1-what-is-a-refresh-token)                               |
| 2   | [Why Refresh Tokens are Needed](#2-why-refresh-tokens-are-needed)                   |
| 3   | [Access Token vs Refresh Token](#3-access-token-vs-refresh-token)                   |
| 4   | [How Refresh Tokens Work](#4-how-refresh-tokens-work)                               |
| 5   | [Refresh Token Flow](#5-refresh-token-flow)                                         |
| 6   | [Implementing Refresh Tokens in FastAPI](#6-implementing-refresh-tokens-in-fastapi) |
| 7   | [Security Best Practices](#7-security-best-practices)                               |
| 8   | [Interview Questions](#8-interview-questions)                                       |

---

# 1. What is a Refresh Token

A **refresh token** is a special token used to generate a **new access token** when the old one expires.

Instead of forcing the user to log in again, the system can **issue a new access token automatically**.

Simple idea:

```text
Access token expired → use refresh token → get new access token
```

---

# 2. Why Refresh Tokens are Needed

Access tokens are intentionally **short-lived** for security.

Example:

```text
Access token lifetime = 15 minutes
```

If there were no refresh tokens:

```text
User would have to login every 15 minutes
```

This would be a bad user experience.

Refresh tokens solve this problem.

---

# 3. Access Token vs Refresh Token

| Feature  | Access Token            | Refresh Token                       |
| -------- | ----------------------- | ----------------------------------- |
| Purpose  | Access APIs             | Generate new access tokens          |
| Lifetime | Short                   | Long                                |
| Usage    | Sent with every request | Used only when access token expires |
| Security | Lower privilege         | Higher protection needed            |

---

### Example

Access token expiration:

```text
15 minutes
```

Refresh token expiration:

```text
7 days
```

---

# 4. How Refresh Tokens Work

When a user logs in, the server generates **two tokens**.

```text
Access Token
Refresh Token
```

Example response:

```json
{
 "access_token": "abc123",
 "refresh_token": "xyz789"
}
```

---

### Token Usage

Client stores both tokens.

For normal API requests:

```text
Use access token
```

When access token expires:

```text
Use refresh token → request new access token
```

---

# 5. Refresh Token Flow

Step-by-step process:

```text
User login
     |
     v
Server generates
Access Token + Refresh Token
     |
     v
Client uses access token
     |
     v
Access token expires
     |
     v
Client sends refresh token
     |
     v
Server verifies refresh token
     |
     v
Server issues new access token
```

---

# 6. Implementing Refresh Tokens in FastAPI

First define expiration times.

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

---

### Create Refresh Token Function

```python
def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)

    data.update({"exp": expire})

    refresh_token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return refresh_token
```

---

### Login Response Example

When user logs in:

```python
return {
 "access_token": access_token,
 "refresh_token": refresh_token,
 "token_type": "bearer"
}
```

Example response:

```json
{
 "access_token": "eyJhbGciOiJIUzI1NiIs...",
 "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
 "token_type": "bearer"
}
```

---

### Refresh Endpoint

Client requests a new token.

```python
@app.post("/refresh")
def refresh_token(refresh_token: str):
    payload = jwt.decode(
        refresh_token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    username = payload.get("sub")

    new_access_token = create_access_token(
        {"sub": username}
    )

    return {
        "access_token": new_access_token
    }
```

---

### Refresh Request Example

Request:

```text
POST /refresh
```

Body:

```json
{
 "refresh_token": "xyz789"
}
```

Response:

```json
{
 "access_token": "new_access_token"
}
```

---

# 7. Security Best Practices

### 1 Store Refresh Tokens Securely

Recommended storage:

* HTTP-only cookies
* secure server storage

Avoid:

```text
Local storage
```

---

### 2 Rotate Refresh Tokens

Every time a refresh token is used:

```text
Generate a new refresh token
```

This prevents replay attacks.

---

### 3 Allow Refresh Token Revocation

If user logs out:

```text
Invalidate refresh token
```

---

### 4 Protect Refresh Endpoint

Refresh endpoint should have:

* rate limiting
* monitoring
* security checks

---

# 8. Interview Questions

### What is a refresh token?

A refresh token is used to generate a new access token when the original access token expires.

---

### Why are refresh tokens used?

Refresh tokens allow users to stay logged in without repeatedly entering their credentials.

---

### What is the difference between access token and refresh token?

Access tokens are short-lived and used for API access, while refresh tokens are long-lived and used to generate new access tokens.

---

### What happens when an access token expires?

The client uses the refresh token to request a new access token.

---

# Summary

Login response:

```text
Access Token + Refresh Token
```

Usage:

```text
Access Token → API access
Refresh Token → generate new access token
```

Security model:

```text
Short-lived access token
Long-lived refresh token
```

---

# Next Part (Part 7)

Next we will learn **RBAC (Role Based Access Control)**.

This is used in real systems like:

* Admin panels
* SaaS applications
* Enterprise software

Example roles:

```text
Admin
Manager
User
```

Each role will have **different permissions**.

This is **very important for backend developers**.
