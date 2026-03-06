

## Route Ordering in FastAPI

In **FastAPI**, the order in which you define routes in your file **matters**. FastAPI checks routes **from top to bottom**, and the first matching route is executed.

FastAPI is built on top of Starlette, and it follows the same routing behavior.


### 📌 Why Route Order Is Important?

If you define a **dynamic route** before a **fixed route**, the dynamic one may capture requests that were meant for the fixed route.


#### Example of Wrong Route Order

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")
def get_current_user():
    return {"user": "current user"}
```

### Problem:

If you visit:

```
/users/me
```

FastAPI will treat `"me"` as `user_id`, because the dynamic route is defined first.

So `/users/me` will never reach the second function.



### ✅ Correct Route Order

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/users/me")
def get_current_user():
    return {"user": "current user"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/greet/{name}")
def greet_name(name: str, age: Optional[int]=None):
    return {"Message": f"Hello {name} and you are {age} years old"}
```

### Why This Works:

* FastAPI checks `/users/me` first.
* If it matches exactly, it runs that function.
* If not, it moves to `/users/{user_id}`.



## Rule to Remember

👉 **Always define fixed (static) routes before dynamic routes.**

Correct order:

1. `/users/me`
2. `/users/settings`
3. `/users/{user_id}`


## How FastAPI Matches Routes

FastAPI:

1. Reads routes top → bottom
2. Matches the first valid path
3. Stops checking further routes

It does **not** try to find the “most specific” route automatically — order decides priority.


## Best Practice for Large Projects

In larger applications:

* Use **APIRouter**
* Group related routes
* Keep static routes above dynamic ones
* Avoid overlapping path structures when possible

Example:

### 📁 Project Structure

```
myproject/
│
├── app/
│   ├── main.py
│   └── routes/
│       ├── __init__.py
│       └── products.py
│
└── requirements.txt
```


### 1️⃣ File: `app/routes/products.py`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/latest")
def get_latest_product():
    return {"product": "latest"}

@router.get("/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}
```

### ✅ What’s happening here?

* `prefix="/products"` → All routes start with `/products`
* So actual paths become:

  * `/products/latest`
  * `/products/{product_id}`
* `tags` helps organize Swagger UI documentation


### 2️⃣ File: `app/main.py`

```python
from fastapi import FastAPI
from app.routes.products import router as product_router

app = FastAPI()

# Include router
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI App"}
```

### 3️⃣ File: `app/routes/__init__.py`

(Empty file – just makes the folder a Python package)

```python
# empty file
```


### Run the Application

```bash
uvicorn app.main:app --reload
```


## 🌐 Available Endpoints

* `GET /`
* `GET /products/latest`
* `GET /products/{product_id}`

Swagger docs:

```
http://127.0.0.1:8000/docs
```