

## Model Creation & Basic Field Validation

### **1. What is Pydantic?**

* **Pydantic** is a Python library used in **FastAPI** for **data validation and settings management** using Python type annotations.
* It ensures that the data you receive or store is **correctly typed and validated** automatically.

**Key Points:**

* Uses **Python type hints**.
* Raises clear **validation errors** if the input is invalid.
* Widely used for **request bodies** in FastAPI.

### **2. Creating a Pydantic Model**

* All models **inherit from `BaseModel`**.
* Fields are defined using **Python type hints**.

**Example:**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True  # default value
```

* Here:

  * `id` must be an integer.
  * `name` must be a string.
  * `email` must be a string.
  * `is_active` is optional because it has a default value `True`.

### **3. Using the Model**

```python
# Creating an instance
user = User(id=1, name="Vinod", email="vinod@example.com")
print(user)
# Output: id=1 name='Vinod' email='vinod@example.com' is_active=True
```

* **Automatic type conversion**:
  If you pass a string for `id`, Pydantic will try to convert it to int.

```python
user = User(id="10", name="Vinod", email="vinod@example.com")
print(user.id)  # 10 (converted from string to int)
```

* **Validation errors**:
  If conversion is impossible:

```python
User(id="abc", name="Vinod", email="vinod@example.com")
# ValidationError: value is not a valid integer
```

### **4. Field Validation (Basic)**

* You can use **type hints** and **Pydantic validators** for validation.
* **Common field types:** `int`, `float`, `str`, `bool`, `list`, `dict`.

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # validates proper email format
```

* Now, if email is invalid:

```python
User(id=1, name="Vinod", email="vinod#example.com")
# ValidationError: value is not a valid email address
```

✅ **Interview Tip:**

* Be prepared to explain why Pydantic is better than plain dictionaries:

  * Type safety
  * Automatic validation
  * Clear error messages
  * Integration with FastAPI request bodies
