

# 1. What is JWT

JWT stands for **JSON Web Token**.

It is a **secure way to transmit information between client and server**.

JWT is commonly used for **authentication in APIs**.

In simple words:

> JWT is a token that proves a user is logged in.

Instead of sending **username and password every time**, the client sends a **token**.

---

### Simple Idea

Traditional login system:

```
Client → username + password → server
```

JWT system:

```
Client → login once
Server → gives JWT token
Client → sends token in every request
```

---

# 2. Why JWT is Used

JWT solves many problems in API authentication.

### 1 Stateless Authentication

Server does not need to store sessions.

Example:

Traditional session system:

```
Server stores session in memory/database
```

JWT system:

```
Token itself contains user data
```

---

### 2 Scalable for Microservices

JWT works well with:

* Microservices
* Cloud systems
* Distributed systems

Because **server does not store session data**.

---

### 3 Secure Communication

JWT uses:

```
Digital signature
```

This ensures:

```
Token cannot be modified
```

---

### 4 API Friendly

JWT is ideal for:

* Mobile apps
* SPAs (React / Angular / Vue)
* REST APIs

---

# 3. Structure of JWT

A JWT token has **3 parts**.

```
HEADER.PAYLOAD.SIGNATURE
```

Example:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.
eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InZpbm9kIn0
.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

---

## Part 1 — Header

Header contains information about:

* token type
* signing algorithm

Example:

```json
{
 "alg": "HS256",
 "typ": "JWT"
}
```

Meaning:

```
Algorithm = HMAC SHA256
Type = JWT
```

---

## Part 2 — Payload

Payload contains **user information**.

Example:

```json
{
 "user_id": 1,
 "username": "vinod",
 "role": "admin"
}
```

This data is called **claims**.

Types of claims:

| Type              | Example  |
| ----------------- | -------- |
| Registered claims | exp, iss |
| Public claims     | username |
| Private claims    | user_id  |

---

## Part 3 — Signature

Signature ensures the token **cannot be changed**.

Signature formula:

```
HMACSHA256(
 base64UrlEncode(header) +
 base64UrlEncode(payload),
 secret_key
)
```

If someone modifies payload → signature becomes invalid.

---

# 4. How JWT Works

Step-by-step JWT process:

### Step 1 — User Login

Client sends credentials.

```
POST /login
```

Request:

```json
{
 "username":"vinod",
 "password":"123456"
}
```

---

### Step 2 — Server Verifies Credentials

Server checks database.

If valid:

```
Server generates JWT token
```

---

### Step 3 — Server Returns Token

Example response:

```json
{
 "access_token": "jwt_token_here",
 "token_type": "bearer"
}
```

---

### Step 4 — Client Stores Token

Client stores token in:

* Local storage
* Cookies
* Memory

---

### Step 5 — Client Sends Token

For protected routes:

```
Authorization: Bearer <token>
```

Example request:

```
GET /profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

---

### Step 6 — Server Validates Token

Server verifies:

* token signature
* expiration
* payload data

If valid → request allowed.

---

# 5. JWT Authentication Flow

```
User Login
     |
     v
Server verifies credentials
     |
     v
Server generates JWT token
     |
     v
Client stores token
     |
     v
Client sends token in request
     |
     v
Server validates token
     |
     v
Access granted
```

---

# 6. JWT Example Token

Example payload:

```json
{
 "user_id": 101,
 "username": "vinod",
 "role": "admin",
 "exp": 1735689600
}
```

Meaning:

| Field    | Meaning            |
| -------- | ------------------ |
| user_id  | user identifier    |
| username | login name         |
| role     | authorization role |
| exp      | expiration time    |

---

# 7. Advantages of JWT

### 1 Stateless

Server does not store session.

---

### 2 Fast

Token verification is quick.

---

### 3 Scalable

Works with distributed systems.

---

### 4 Secure

Signed tokens prevent tampering.

---

### 5 Cross-platform

Works with:

* Web apps
* Mobile apps
* APIs

---

# 8. JWT vs Session Authentication

| Feature       | JWT          | Session     |
| ------------- | ------------ | ----------- |
| Storage       | Client side  | Server side |
| Scalability   | High         | Limited     |
| Microservices | Good         | Difficult   |
| Server memory | Not required | Required    |

---

# 9. Interview Questions

### What is JWT?

JWT is a compact token format used to securely transmit information between client and server for authentication.

---

### What are the three parts of JWT?

JWT consists of:

1 Header
2 Payload
3 Signature

---

### Why JWT is used in APIs?

JWT is used because it enables **stateless authentication**, making APIs scalable and secure.

---

### What does the payload contain?

Payload contains **claims**, which store user information such as user id, username, roles, and expiration time.

---

# Summary

JWT structure:

```
Header.Payload.Signature
```

Used for:

```
API Authentication
Stateless login
Secure token verification
```