Now we continue with **Part 5** of Chapter 7.
This part focuses on **Token Expiration**, which is very important for **security in real-world APIs**.

---

# Chapter 7: Authentication & Authorization (Part 5)

## Token Expiration

| No. | Topic                                                                                   |
| --- | --------------------------------------------------------------------------------------- |
| 1   | [What is Token Expiration](#1-what-is-token-expiration)                                 |
| 2   | [Why Token Expiration is Important](#2-why-token-expiration-is-important)               |
| 3   | [JWT Expiration Claim (exp)](#3-jwt-expiration-claim-exp)                               |
| 4   | [How Token Expiration Works](#4-how-token-expiration-works)                             |
| 5   | [Implementing Token Expiration in FastAPI](#5-implementing-token-expiration-in-fastapi) |
| 6   | [Handling Expired Tokens](#6-handling-expired-tokens)                                   |
| 7   | [Best Practices for Token Expiration](#7-best-practices-for-token-expiration)           |
| 8   | [Interview Questions](#8-interview-questions)                                           |

---

# 1. What is Token Expiration

Token expiration means that a **JWT token is only valid for a limited time**.

After the time limit is reached:

```text
Token becomes invalid
```

The user must **log in again** or use a **refresh token**.

---

### Example

A token created at:

```text
10:00 AM
```

Expiration time:

```text
10:30 AM
```

After **10:30 AM**, the token cannot be used.

---

# 2. Why Token Expiration is Important

Without expiration, tokens could be used forever.

Example risk:

```text
If attacker steals token → permanent access
```

Token expiration improves security because:

* stolen tokens eventually stop working
* users must re-authenticate
* reduces long-term security risks

---

### Real Example

Websites like:

* Google
* GitHub
* Amazon

All use **token expiration**.

---

# 3. JWT Expiration Claim (exp)

JWT includes a special claim:

```text
exp
```

This stands for **expiration time**.

Example payload:

```json
{
 "sub": "vinod",
 "exp": 1735689600
}
```

Meaning:

| Field | Meaning              |
| ----- | -------------------- |
| sub   | subject (user)       |
| exp   | expiration timestamp |

The timestamp is in **Unix time**.

---

# 4. How Token Expiration Works

Step-by-step process:

1. Server generates token
2. Token includes expiration time
3. Client sends token with requests
4. Server checks expiration
5. If expired → request rejected

---

### Authentication Flow

```
User login
     |
     v
Server creates JWT with expiration
     |
     v
Client sends token in requests
     |
     v
Server checks token validity
     |
     v
If expired → access denied
```

---

# 5. Implementing Token Expiration in FastAPI

We add expiration when creating the token.

Example:

```python
from datetime import datetime, timedelta
```

---

### Token Creation Function

```python
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
```

---

### What Happens Here

Step 1:

```python
expire = datetime.utcnow() + timedelta(minutes=30)
```

Token expires in **30 minutes**.

---

Step 2:

```python
to_encode.update({"exp": expire})
```

Adds expiration claim to JWT payload.

---

Step 3:

```python
jwt.encode(...)
```

Creates the token.

---

# 6. Handling Expired Tokens

When the client sends an expired token:

```text
jwt.decode() throws an error
```

Example code:

```python
from jose import JWTError
```

---

### Token Validation

```python
try:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
except JWTError:
    raise Exception("Token expired or invalid")
```

If expired → request rejected.

---

### Response Example

```
401 Unauthorized
```

Example message:

```json
{
 "detail": "Token expired"
}
```

---

# 7. Best Practices for Token Expiration

### 1 Use Short Expiration for Access Tokens

Example:

| Token Type    | Expiration    |
| ------------- | ------------- |
| Access Token  | 15–30 minutes |
| Refresh Token | 7–30 days     |

---

### 2 Use Refresh Tokens

Instead of forcing login again, use refresh tokens.

We will learn this in **Part 6**.

---

### 3 Protect Tokens

Tokens should be stored securely:

Recommended storage:

* HTTP-only cookies
* secure storage in mobile apps

Avoid:

* exposing tokens in URLs

---

### 4 Rotate Tokens

Large systems rotate tokens regularly.

---

# 8. Interview Questions

### What is token expiration?

Token expiration is the time limit after which a JWT token becomes invalid and cannot be used for authentication.

---

### Which JWT claim defines expiration?

The **exp claim** defines the expiration time.

---

### Why is token expiration important?

Token expiration improves security by limiting the lifetime of authentication tokens.

---

### What happens when a token expires?

The server rejects the request and returns **401 Unauthorized**.

---

# Summary

Token creation:

```
JWT = Header + Payload + Signature
```

Payload includes:

```
sub → user
exp → expiration time
```

Authentication rule:

```
If token expired → access denied
```

---

# Next Part (Part 6)

Next we will learn **Refresh Tokens**, which are used in almost every **production API**.

Topics:

* Access token vs refresh token
* Why refresh tokens exist
* Refresh token flow
* Implementing refresh tokens in FastAPI

This is an **important concept used in systems like Google, Facebook, and GitHub APIs**.
