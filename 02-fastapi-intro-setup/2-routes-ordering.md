<style> h1 { color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px 25px; border-radius: 10px; text-align: center; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); } h2 { color: #fff; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px 20px; border-radius: 8px; border-left: 5px solid #ff1744; box-shadow: 0 4px 10px rgba(245, 87, 108, 0.3); } h3 { color: #667eea; border-left: 4px solid #667eea; padding-left: 15px; } li { color: #444; margin: 12px 0; } li::marker { color: #f5576c; font-weight: bold; } strong { color: #f5576c; font-weight: 600; } code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; color: #c7254e; } pre { background: #2d2d2d; color: #f8f8f2; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; } table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); } th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-bottom: 3px solid #f5576c; } td { padding: 12px 15px; border-bottom: 1px solid #e0e0e0; } tr:hover { background: #f9f9f9; } hr { border: none; height: 3px; background: linear-gradient(to right, #667eea, #764ba2, #f5576c); border-radius: 2px; } blockquote { background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%); border-left: 5px solid #667eea; padding: 20px 25px; border-radius: 8px; } </style>

# Route Ordering in FastAPI

In **FastAPI**, the order in which you define routes in your file **matters**. FastAPI checks routes **from top to bottom**, and the first matching route is executed.

FastAPI is built on top of Starlette, and it follows the same routing behavior.


## 🔹 Why Route Order Is Important?

If you define a **dynamic route** before a **fixed route**, the dynamic one may capture requests that were meant for the fixed route.


### Example of Wrong Route Order

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

app = FastAPI()

@app.get("/users/me")
def get_current_user():
    return {"user": "current user"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}
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