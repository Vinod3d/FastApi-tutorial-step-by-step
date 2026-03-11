Now we move to **Part 7** of Chapter 7.
In this part we will learn **RBAC (Role Based Access Control)**, which is used in almost every **real production backend**.

---

# Chapter 7: Authentication & Authorization (Part 7)

## RBAC (Role Based Access Control)

| No. | Topic                                                                     |
| --- | ------------------------------------------------------------------------- |
| 1   | [What is RBAC](#1-what-is-rbac)                                           |
| 2   | [Why RBAC is Used](#2-why-rbac-is-used)                                   |
| 3   | [Roles and Permissions](#3-roles-and-permissions)                         |
| 4   | [RBAC Example in Real Applications](#4-rbac-example-in-real-applications) |
| 5   | [Implementing RBAC in FastAPI](#5-implementing-rbac-in-fastapi)           |
| 6   | [Creating Role-Based Dependency](#6-creating-role-based-dependency)       |
| 7   | [Protecting Routes with Roles](#7-protecting-routes-with-roles)           |
| 8   | [Interview Questions](#8-interview-questions)                             |

---

# 1. What is RBAC

RBAC stands for **Role Based Access Control**.

It is a method used to **control what actions users can perform based on their role**.

In simple words:

```text
User → assigned a role
Role → defines permissions
```

---

### Example

A system may have these roles:

```text
Admin
Manager
User
```

Each role has different permissions.

---

# 2. Why RBAC is Used

RBAC helps manage permissions efficiently.

Without RBAC:

```text
Permissions assigned individually to each user
```

This becomes difficult to manage.

With RBAC:

```text
Permissions assigned to roles
Users assigned to roles
```

This makes systems easier to maintain.

---

# 3. Roles and Permissions

Two key concepts:

### Role

A role represents a **user category**.

Examples:

```text
Admin
Editor
Customer
```

---

### Permission

Permissions define **what actions are allowed**.

Examples:

```text
create_user
delete_user
view_orders
update_product
```

---

### Role Permission Example

| Role   | Permissions            |
| ------ | ---------------------- |
| Admin  | create, update, delete |
| Editor | create, update         |
| User   | read only              |

---

# 4. RBAC Example in Real Applications

Example: **E-commerce system**

| Role     | Access                 |
| -------- | ---------------------- |
| Admin    | manage users, products |
| Seller   | manage products        |
| Customer | view and buy products  |

---

Example API routes:

```text
GET /products
POST /products
DELETE /products/{id}
```

Permissions:

| Role     | Allowed Actions |
| -------- | --------------- |
| Admin    | all routes      |
| Seller   | GET, POST       |
| Customer | GET only        |

---

# 5. Implementing RBAC in FastAPI

First we include role in the **JWT token payload**.

Example payload:

```json
{
 "sub": "vinod",
 "role": "admin"
}
```

When decoding the token, we retrieve the role.

---

### Example User Database

```python
fake_users_db = {
    "vinod": {
        "username": "vinod",
        "role": "admin"
    },
    "rahul": {
        "username": "rahul",
        "role": "user"
    }
}
```

---

# 6. Creating Role-Based Dependency

We create a function that checks user role.

Example:

```python
from fastapi import Depends, HTTPException
```

---

### Role Check Function

```python
def require_role(required_role: str):

    def role_checker(user=Depends(get_current_user)):

        if user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    return role_checker
```

This dependency ensures only users with the correct role can access the route.

---

# 7. Protecting Routes with Roles

Now we protect routes.

Example:

```python
@app.delete("/users/{id}")
def delete_user(
    user = Depends(require_role("admin"))
):
    return {"message": "User deleted"}
```

Only **admin users** can access this route.

---

### Example Request

```text
DELETE /users/10
Authorization: Bearer <token>
```

---

### Response (Admin)

```json
{
 "message": "User deleted"
}
```

---

### Response (Normal User)

```json
{
 "detail": "Access denied"
}
```

---

# 8. Interview Questions

### What is RBAC?

RBAC (Role Based Access Control) is a security model that controls user access based on assigned roles.

---

### Why is RBAC used?

RBAC simplifies permission management by assigning permissions to roles instead of individual users.

---

### What are roles and permissions?

Roles define user categories, while permissions define what actions users can perform.

---

### How is RBAC implemented in FastAPI?

RBAC can be implemented by including roles in JWT tokens and using dependency functions to restrict access to specific routes.

---

# Summary

RBAC system:

```text
User → assigned role
Role → defines permissions
Permissions → control API access
```

Example roles:

```text
Admin → full access
Manager → limited access
User → read only
```

RBAC is commonly used in:

* Admin dashboards
* SaaS platforms
* Enterprise applications

---

# Next Part (Final Part)

Next we will learn **OAuth2 Scopes**, which are used for **fine-grained permission control**.

Example scopes:

```text
read:user
write:user
delete:user
```

Scopes are used by APIs like:

* Google API
* GitHub API
* Stripe API

This will be the **final part of Chapter 7**.
