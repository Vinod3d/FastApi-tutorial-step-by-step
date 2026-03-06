

# Path Parameters

### ✅ What are Path Parameters?

Path parameters are dynamic values that are part of the URL path.

Example:

```
/users/10
/products/5
/orders/101
```

Here, `10`, `5`, `101` are path parameters.

#### Basic Example in FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

#### 🔎 How it works:

* `{user_id}` is a path parameter
* FastAPI automatically converts it to `int`
* If conversion fails → validation error


#### ✅ Automatic Validation

If you call:

```
/users/abc
```

You will get:

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

👉 FastAPI uses Pydantic validation internally.

#### ✅ Multiple Path Parameters

```python
@app.get("/users/{user_id}/orders/{order_id}")
def get_order(user_id: int, order_id: int):
    return {
        "user_id": user_id,
        "order_id": order_id
    }
```
#### ✅ Path Parameter with Validation

We use `Path()` for advanced validation.

```python
from fastapi import Path

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., gt=0, lt=1000)
):
    return {"item_id": item_id}
```

### 🔎 Meaning:

* `...` → required
* `gt=0` → greater than 0
* `lt=1000` → less than 1000

---

# Query Parameters

### ✅ What are Query Parameters?

Query parameters come after `?` in URL.

Example:

```
/users?limit=10
/products?category=electronics
/items?page=2&size=20
```


#### Basic Example

```python
@app.get("/users")
def get_users(limit: int = 10):
    return {"limit": limit}
```

Call:

```
/users?limit=5
```

#### ✅ Optional Query Parameters

```python
from typing import Optional

@app.get("/products")
def get_products(category: Optional[str] = None):
    return {"category": category}
```

If not provided → `None`

#### ✅ Multiple Query Parameters

```python
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }
```

#### ✅ Query Parameter Validation

Using `Query()`:

```python
from fastapi import Query

@app.get("/search")
def search_items(
    q: str = Query(..., min_length=3, max_length=50)
):
    return {"query": q}
```

### 🔎 Meaning:

* `...` → required
* `min_length=3`
* `max_length=50`



#### ✅ Use Path Parameter when:

* Identifying specific resource
* Required to locate object

Example:

```
/users/{id}
```

#### ✅ Use Query Parameter when:

* Filtering
* Sorting
* Pagination
* Searching

Example:

```
/users?age=25&city=Delhi
```

#### 🔥 Advanced Interview Concept

You can mix both:

```python
@app.get("/users/{user_id}")
def get_user_orders(
    user_id: int,
    page: int = 1,
    size: int = 10
):
    return {
        "user_id": user_id,
        "page": page,
        "size": size
    }
```