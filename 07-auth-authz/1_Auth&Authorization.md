

## 1. What is Authentication

### Definition

**Authentication** is the process of verifying the identity of a user.

In simple words:

> Authentication answers the question: **"Who are you?"**

The system checks whether the user is really the person they claim to be.

---

### Example

When you log into a website:

1. You enter **username/email**
2. You enter **password**
3. Server verifies credentials
4. If correct → user is authenticated

Example websites:

* Gmail
* Facebook
* GitHub
* Amazon

All these perform authentication before giving access.

---

### Authentication Methods

Common authentication methods:

| Method    | Example               |
| --------- | --------------------- |
| Password  | Email + Password      |
| OTP       | Mobile OTP            |
| Biometric | Fingerprint / Face ID |
| API Key   | API access            |
| Token     | JWT token             |

---

### Simple Authentication Flow

```
User → Login request
        |
        v
Server verifies credentials
        |
        v
If valid → Authentication successful
```

---

### Real Example

Login to an e-commerce site:

```
Email: vinod@gmail.com
Password: ********
```

Server checks database:

```
users table
-------------------------
id | email | password
-------------------------
1  | vinod@gmail.com | hashed_password
```

If password matches → user authenticated.

---

# 2. What is Authorization

### Definition

**Authorization** decides **what a user is allowed to do**.

In simple words:

> Authorization answers the question: **"What can you do?"**

---

### Example

Suppose a system has:

| User     | Role           |
| -------- | -------------- |
| Admin    | Full access    |
| Employee | Limited access |
| Customer | View only      |

After authentication, authorization decides:

* Can the user delete data?
* Can the user view reports?
* Can the user access admin panel?

---

### Real Example

Example: **Blog Website**

Users:

| Role   | Permission               |
| ------ | ------------------------ |
| Admin  | create/edit/delete posts |
| Author | create/edit posts        |
| User   | read posts               |

---

### Authorization Flow

```
User logged in (authenticated)
         |
         v
Server checks role/permission
         |
         v
Allow / Deny action
```

---

# 3. Difference Between Authentication and Authorization

| Feature  | Authentication  | Authorization                |
| -------- | --------------- | ---------------------------- |
| Meaning  | Verify identity | Check permissions            |
| Question | Who are you?    | What can you do?             |
| Example  | Login           | Access control               |
| Step     | Happens first   | Happens after authentication |

---

### Example Scenario

User logs into system.

Step 1 → Authentication

```
Email + Password verified
```

Step 2 → Authorization

```
Admin → can delete users
Normal user → cannot delete users
```

---

# 4. Authentication in Real Applications

Typical login system works like this:

```
User enters credentials
       |
       v
Server verifies password
       |
       v
Server creates token/session
       |
       v
User can access protected routes
```

Example protected routes:

```
/profile
/orders
/dashboard
/settings
```

If user not authenticated:

```
401 Unauthorized
```

---

# 5. Authorization in Real Applications

Example:

```
DELETE /users/10
```

System checks:

```
Is user admin?
```

If yes:

```
Action allowed
```

If not:

```
403 Forbidden
```

---

# 6. Authentication in FastAPI

FastAPI supports many authentication systems:

1️⃣ **Basic Auth**

```
username + password
```

2️⃣ **OAuth2**

Used in modern APIs.

3️⃣ **JWT Authentication**

Most popular for APIs.

4️⃣ **API Keys**

Used for services.

---

### Example Protected Route

```
GET /profile
```

Only authenticated users can access it.

Example response:

```json
{
"id":1,
"name":"Vinod",
"email":"vinod@gmail.com"
}
```

---

# 7. Authorization in FastAPI

FastAPI supports authorization methods like:

### Role Based Access Control (RBAC)

Example roles:

```
Admin
Manager
User
```

Example rule:

```
Admin → delete users
User → cannot delete users
```

Example route:

```
DELETE /users/{id}
```

Allowed only for **admin**.

---

# 8. Interview Questions

### 1️⃣ What is Authentication?

Authentication is the process of verifying the identity of a user before allowing access to a system.

---

### 2️⃣ What is Authorization?

Authorization is the process of determining what actions a user is allowed to perform after authentication.

---

### 3️⃣ What is the difference between Authentication and Authorization?

Authentication verifies **who the user is**, while authorization determines **what the user is allowed to do**.

---

### 4️⃣ What are common authentication methods?

Common authentication methods include:

* Password based authentication
* OTP authentication
* Biometric authentication
* Token based authentication (JWT)

---

# Summary

Authentication:

```
Identity verification
```

Authorization:

```
Access control
```

Both are essential for building **secure APIs and applications**.

---

# Next Part

In **Part 2** we will learn:

* What is **JWT**
* Why JWT is used
* Structure of JWT
* How JWT works internally
* Real FastAPI JWT example

This is where **real authentication implementation begins.**
