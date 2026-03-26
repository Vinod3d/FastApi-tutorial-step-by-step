# Request Body & Pydantic Validation

## What you will learn
- How to receive data payloads from clients (POST/PUT requests)
- How to define Pydantic Models for data validation
- Handling Required vs Optional fields
- Understanding nested models for complex JSON

## Concept (Simple Explanation)
While Path and Query parameters are good for sending tiny bits of information (like IDs or search terms), they aren't enough when you need to send a massive form, like registering a new user with an address, password, and preferences.

The **Request Body** is the "envelope" where clients place large amounts of data (usually JSON format). In FastAPI, we create a strict blueprint (a **Pydantic Model**) that acts like a bouncer at a club—it checks the data inside the envelope perfectly matches the rules before letting it into your code.



# Request Body

## 1️⃣ What is a Request Body?

A request body is used to **send data from client to server**, usually in:

* `POST`
* `PUT`
* `PATCH`

The data is typically sent in **JSON format**.

Example JSON:

```json
{
  "name": "Vinod",
  "age": 25
}
```

## 2️⃣ How FastAPI Handles Request Body

FastAPI uses **Pydantic models** to:

* Validate input data
* Convert data types
* Generate API documentation automatically
* Raise validation errors if data is incorrect


## ✅ Basic Example

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return {"message": "User created", "data": user}
```

### 🔎 What happens internally?

1. FastAPI reads JSON body
2. Converts it into `User` model
3. Validates types
4. If invalid → returns 422 error automatically


## 3️⃣ Automatic Validation Example

If request is:

```json
{
  "name": "Vinod",
  "age": "twenty"
}
```

Response:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "msg": "Input should be a valid integer"
    }
  ]
}
```

👉 You don’t write validation manually. FastAPI handles it.

## 4️⃣ Required vs Optional Fields

```python
from typing import Optional

class User(BaseModel):
    name: str
    age: Optional[int] = None
```

* `name` → required
* `age` → optional


## 5️⃣ Default Values

```python
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True
```

If `in_stock` not sent → default `True`


## 6️⃣ Nested Models

Real-world APIs often have nested objects.

Example JSON:

```json
{
  "name": "Vinod",
  "age": 25,
  "address": {
    "city": "Lucknow",
    "pincode": "226001"
  }
}
```

### Model:

```python
class Address(BaseModel):
    city: str
    pincode: str

class User(BaseModel):
    name: str
    age: int
    address: Address
```

FastAPI automatically validates nested structure.

# 🔥 Interview Question

### ❓ What happens if nested field is wrong?

If:

```json
"address": {
  "city": 123,
  "pincode": "226001"
}
```

FastAPI returns validation error for `city`.

## 7️⃣ List in Request Body

Example JSON:

```json
{
  "name": "Order1",
  "items": ["apple", "banana"]
}
```

Model:

```python
from typing import List

class Order(BaseModel):
    name: str
    items: List[str]
```

## 8️⃣ Multiple Body Parameters

Normally FastAPI expects one body model.

But you can do:

```python
class User(BaseModel):
    name: str

class Profile(BaseModel):
    bio: str

@app.post("/create")
def create(user: User, profile: Profile):
    return {"user": user, "profile": profile}
```

Then request body must be:

```json
{
  "user": { "name": "Vinod" },
  "profile": { "bio": "Developer" }
}
```

## 9️⃣ Body with Path and Query Parameters Together

```python
@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: User,
    notify: bool = False
):
    return {
        "user_id": user_id,
        "data": user,
        "notify": notify
    }
```

* `user_id` → Path parameter
* `notify` → Query parameter
* `user` → Request body

👉 FastAPI automatically understands by position and type.


## 10️⃣ Using Body() Explicitly

```python
from fastapi import Body

@app.post("/items")
def create_item(
    name: str = Body(...),
    price: float = Body(..., gt=0)
):
    return {"name": name, "price": price}
```

Used when not using Pydantic model.


# 🔥 Important Interview Concepts

### ✅ When does FastAPI treat parameter as Body?

If:

* It is a Pydantic model
* Or explicitly wrapped with `Body()`

Otherwise:

* Simple types → Query parameters


### ✅ Difference Between Query and Body

| Query               | Body                      |
| ------------------- | ------------------------- |
| Small data          | Complex data              |
| Filters, pagination | Create/update data        |
| Visible in URL      | Hidden in request payload |

# 🚨 Common Mistakes

❌ Forgetting Pydantic model
❌ Not handling optional fields properly
❌ Mixing up query and body
❌ Not validating numeric ranges

## Best Practices
- **Think in Objects:** Avoid extracting raw dictionaries from the request. Always mold the incoming JSON into Pydantic BaseModels so you get full IDE autocomplete and type safety throughout your app.
- **Use `model_dump()`:** When you need to turn the Pydantic object back into a dictionary (for instance, to pass it to a database ORM), use `user.model_dump()` (or `.dict()` in older versions of Pydantic).

## Common Mistakes
- **Sending Body data in a GET request:** Technically HTTP allows this, but it is heavily discouraged and many proxies/servers will drop the body. Use POST, PUT, or PATCH when you need a request body.
- **Assuming FastAPI will parse complex dicts without a model:** If you declare a parameter as `data: dict`, FastAPI will accept *any* JSON object without validation. This defeats the purpose of the framework! Define strict BaseModels.

## Interview Questions
**Q: When does FastAPI treat a function argument as a Request Body instead of a Query Parameter?**
A: If the parameter's type is declared as a Pydantic `BaseModel` (or explicitly wrapped using `Body()`), FastAPI knows to look for it in the JSON request body. Simple types (int, str) default to Query parameters.

**Q: In the UserCreate model, what happens if the client sends `"age": "twenty"` in the JSON payload?**
A: Because Pydantic strictly enforces types, it will fail to cast "twenty" into an integer. It immediately rejects the request and returns an automatic `422 Unprocessable Entity` error detailing exactly which field failed and why.
