

#  HTTP Methods in FastAPI (GET, POST, PUT, PATCH, DELETE)

Understanding HTTP methods is **very important for interviews** because they test your knowledge of REST API design principles.


## 1️⃣ What is an HTTP Method?

An HTTP method tells the server **what action** you want to perform on a resource.

Example resource:

```
/users
/products
/orders
```

## 2️⃣ GET Method

Used to **retrieve data** from the server.

### 🔹 Characteristics:

* Does NOT modify data
* Safe and idempotent
* Data usually sent via query parameters
* No request body (by convention)

### 🔹 Example in FastAPI:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    # type hint of id 👆 
    # used for validation
    return {
        "id": id,
        "weight": 1.2,
        "content": "wooden table",
        "status": "in transit"
    }
```

### 🔹 Interview Points:

* GET should not change database state.
* It can be cached.
* It is idempotent (multiple calls → same result).

## 3️⃣ POST Method

Used to **create a new resource**.

### 🔹 Characteristics:

* Modifies server data
* Not idempotent
* Data sent via request body

### 🔹 Example:

```python
from pydantic import BaseModel

@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, int]:
    # Validate weight
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kgs"
        )
    # Create and assign shipment a new id
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": content,
        "weight": weight,
        "status": "placed",
    }
    # Return id for later use
    return {"id": new_id}
```

### 🔹 Interview Points:

* Used when creating new database records.
* Usually returns `201 Created`.
* Multiple identical requests → multiple resources created.

## 4️⃣ PUT Method

Used to **completely update** a resource.

### 🔹 Characteristics:

* Idempotent
* Replaces full resource

### 🔹 Example:

```python
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    return {"message": f"User {user_id} updated", "data": user}
```

### 🔹 Interview Points:

* Entire resource is replaced.
* If field missing → it may get removed.
* Idempotent (same request → same result).

## 5️⃣ PATCH Method

Used to **partially update** a resource.

### 🔹 Characteristics:

* Only updates provided fields
* Not necessarily idempotent

### 🔹 Example:

```python
class UserUpdate(BaseModel):
    name: str | None = None
    age: int | None = None

@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserUpdate):
    return {"message": f"User {user_id} partially updated", "data": user}
```

### 🔹 Interview Points:

* Only modifies given fields.
* Useful when updating small parts of large objects.


## 6️⃣ DELETE Method

### 🔹 Purpose:

Used to **remove a resource**.

### 🔹 Example:

```python
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
```

### 🔹 Interview Points:

* Usually returns `204 No Content`.
* Idempotent (deleting same item multiple times → same state).

# 🔥 Important Interview Question

### ❓ Difference between PUT and PATCH?

| PUT                      | PATCH                   |
| ------------------------ | ----------------------- |
| Full update              | Partial update          |
| Idempotent               | Not always              |
| Replaces entire resource | Updates selected fields |

# 🧠 REST API Design Rule

For a `/users` resource:

| Action         | Method | Endpoint      |
| -------------- | ------ | ------------- |
| Get all users  | GET    | `/users`      |
| Get one user   | GET    | `/users/{id}` |
| Create user    | POST   | `/users`      |
| Update user    | PUT    | `/users/{id}` |
| Partial update | PATCH  | `/users/{id}` |
| Delete user    | DELETE | `/users/{id}` |