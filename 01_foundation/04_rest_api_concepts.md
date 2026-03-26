# REST API Concepts

## What you will learn
- What an API actually is
- The core principles of REST
- The difference between HTTP Methods (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
- What "Statelessness" means in APIs

## Concept (Simple Explanation)
An API (Application Programming Interface) is like a waiter in a restaurant. You (the client) give your order to the waiter (the API), the waiter takes it to the kitchen (the server/database), and brings your food (the response) back to you.

**REST** (Representational State Transfer) is a set of rules for how that waiter should behave. It says the waiter shouldn't have a memory of your past orders (Stateless), should use standard verbs like "Fetch Menu", "Place Order", "Cancel Order" (Uniform Interface), and should treat every item (Users, Orders, Products) as standard resources.

## Code Example
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# A simple in-memory database
users_db = {1: {"name": "Vinod", "role": "admin"}}

# 1. GET: Retrieve Data
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

# 2. POST: Create Data
@app.post("/users")
async def create_user(user_id: int, name: str, role: str):
    users_db[user_id] = {"name": name, "role": role}
    return {"message": "User created!"}

# 3. PUT: Replace Entire Data
@app.put("/users/{user_id}")
async def replace_user(user_id: int, name: str, role: str):
    users_db[user_id] = {"name": name, "role": role}
    return {"message": "User fully updated!"}

# 4. DELETE: Remove Data
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    users_db.pop(user_id, None)
    return {"message": "User deleted!"}
```

## Best Practices
- **Resource Naming:** Use plural nouns for endpoints. Use `/users` instead of `/get_user` or `/create_user`. The HTTP method (`GET`, `POST`) already tells you the action.
- **Versioning:** Always version your APIs (`/v1/users`, `/v2/users`) so you can make breaking changes in the future without destroying old client applications.

## Common Mistakes
- **Misusing POST vs PUT vs PATCH:** 
  - `POST` creates a brand new resource.
  - `PUT` replaces the *entire* existing resource. If you send missing fields, they should be overwritten with blanks/nulls.
  - `PATCH` updates *only* specific fields provided, leaving the rest untouched.
- **Storing Session Data on Server:** A true REST API is stateless. Never use backend sessions; instead, use JWT (JSON Web Tokens) that the client sends with every request.

## Interview Questions
**Q: What is the difference between PUT and PATCH?**
A: `PUT` replaces the entire resource. If you omit a field in a `PUT` request, it should theoretically be deleted or set to null. `PATCH` performs a partial update, modifying only the fields you explicitly send.

**Q: What does "Idempotent" mean in REST?**
A: An idempotent HTTP method is one where making the identical request multiple times has the same effect as making it once. `GET`, `PUT`, and `DELETE` are idempotent. `POST` is not (calling it 5 times creates 5 new resources).

**Q: Why is REST preferred over older protocols like SOAP?**
A: REST is much more lightweight, uses simple HTTP verbs, uses JSON instead of bulky XML, and is much faster for modern web and mobile applications.
