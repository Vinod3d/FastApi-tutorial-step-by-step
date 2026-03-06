

# Status Codes

Status codes tell the client **what happened** after making a request.

Understanding correct status codes is very important in interviews and real-world API design.



# 1️⃣ What is a Status Code?

An HTTP status code is a 3-digit number returned by the server.

Example:

```
200
201
404
500
```

They are divided into categories:

| Range | Meaning       |
| ----- | ------------- |
| 1xx   | Informational |
| 2xx   | Success       |
| 3xx   | Redirection   |
| 4xx   | Client Error  |
| 5xx   | Server Error  |

In FastAPI, we mostly use **2xx, 4xx, 5xx**.

## 2️⃣ Default Status Codes in FastAPI

If you don’t specify anything:

| Method | Default Status Code |
| ------ | ------------------- |
| GET    | 200 OK              |
| POST   | 200 OK              |
| PUT    | 200 OK              |
| PATCH  | 200 OK              |
| DELETE | 200 OK              |

But this is NOT always correct REST practice.


## 3️⃣ Commonly Used Status Codes

## ✅ 200 OK

Request successful (GET, PUT, PATCH)

```python
@app.get("/users")
def get_users():
    return {"message": "Success"}
```


## ✅ 201 Created

Used when a new resource is created.

```python
@app.post("/users", status_code=201)
def create_user(user: User):
    return user
```

Better REST practice:
POST → 201


## ✅ 204 No Content

Used when request successful but no response body.

Common for DELETE.

```python
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    return
```

Important:
204 → No response body allowed.

## ❌ 400 Bad Request

Client sent invalid request (manual validation case)



## ❌ 401 Unauthorized

Authentication required.



## ❌ 403 Forbidden

Authenticated but not allowed.



## ❌ 404 Not Found

Resource does not exist.

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id}
```



## ❌ 422 Unprocessable Entity

Very important.

FastAPI returns 422 when:

* Path parameter validation fails
* Query parameter validation fails
* Body validation fails

You do NOT manually raise this normally.



## ❌ 500 Internal Server Error

Server crash / unhandled exception.



## 4️⃣ How to Set Status Code in FastAPI

### Method 1: Using decorator

```python
@app.post("/users", status_code=201)
```

### Method 2: Using Response object

```python
from fastapi import Response

@app.post("/users")
def create_user(user: User, response: Response):
    response.status_code = 201
    return user
```

## 5️⃣ Raising Custom Errors

Use `HTTPException`.

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID"
        )
    return {"item_id": item_id}
```

# 🔥 Interview Design Best Practices

For a `/users` resource:

| Action         | Method | Status Code |
| -------------- | ------ | ----------- |
| Get all        | GET    | 200         |
| Get one        | GET    | 200 / 404   |
| Create         | POST   | 201         |
| Update         | PUT    | 200         |
| Partial Update | PATCH  | 200         |
| Delete         | DELETE | 204         |


# 🔥 Common Interview Questions

### ❓ Difference between 400 and 422?

* 400 → Client sends bad request manually validated
* 422 → Validation error by FastAPI/Pydantic



### ❓ Why use 201 instead of 200 for POST?

Because resource is newly created.



### ❓ When should we return 204?

When:

* Successful delete
* No response body needed


# 🚨 Common Mistakes

❌ Returning 200 for everything
❌ Returning body with 204
❌ Not raising 404 for missing resource
❌ Confusing 401 and 403


# 🎯 Important Concept for Senior-Level Interviews

Good API design = Correct HTTP method + Correct status code.