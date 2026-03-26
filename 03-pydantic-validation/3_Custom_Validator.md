## Custom Validators, Advanced Field Validation, and Serialization

### **1. Custom Validators**

* Pydantic allows **custom validation logic** using the `@validator` decorator.
* Useful for **complex rules** that type hints alone cannot enforce.

**Example: Validate a username length**

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    id: int
    name: str
    email: str

    @validator('name')
    def name_must_be_long(cls, v):
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters')
        return v
```

**Usage:**

```python
User(id=1, name="Vi", email="vinod@example.com")
# ValidationError: Name must be at least 3 characters

User(id=1, name="Vinod", email="vinod@example.com")
# Success
```

### **2. Multiple Field Validation**

* You can validate **multiple fields together** using `@root_validator`.

```python
from pydantic import BaseModel, root_validator

class User(BaseModel):
    password: str
    confirm_password: str

    @root_validator
    def passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw != cpw:
            raise ValueError('Passwords do not match')
        return values
```

**Usage:**

```python
User(password="1234", confirm_password="12345")
# ValidationError: Passwords do not match
```

✅ **Interview Tip:**

* `@validator` → single field validation
* `@root_validator` → multiple fields inter-dependent validation

### **3. Serialization (model → dict / JSON)**

* Pydantic models can be **converted easily to dict or JSON**.
* Useful for **responses in FastAPI**.

```python
user = User(id=1, name="Vinod", email="vinod@example.com")
print(user.dict())  
# {'id': 1, 'name': 'Vinod', 'email': 'vinod@example.com'}

print(user.json())  
# '{"id": 1, "name": "Vinod", "email": "vinod@example.com"}'
```

* You can **exclude fields** if needed:

```python
user.dict(exclude={"email"})
# {'id': 1, 'name': 'Vinod'}
```

* Or **include only certain fields**:

```python
user.dict(include={"name"})
# {'name': 'Vinod'}
```

### **4. Advanced Field Validation Using Pydantic Types**

* Pydantic provides **special types** for common use cases:

| Type          | Purpose                                  |
| ------------- | ---------------------------------------- |
| `EmailStr`    | Validates correct email format           |
| `HttpUrl`     | Validates URL                            |
| `PositiveInt` | Integer > 0                              |
| `conint`      | Constrained int (e.g., min/max value)    |
| `constr`      | Constrained string (length, regex, etc.) |

**Example: Email & Age validation**

```python
from pydantic import BaseModel, EmailStr, PositiveInt, constr

class User(BaseModel):
    name: constr(min_length=3, max_length=50)
    email: EmailStr
    age: PositiveInt
```

* ✅ This ensures fields are **validated automatically** without custom validators in most cases.


### **5. Real-world Example: User Registration**

```python
from pydantic import BaseModel, EmailStr, validator

class UserRegistration(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

# Serialize to JSON for API response
user = UserRegistration(
    username="Vinod",
    email="vinod@example.com",
    password="mypassword",
    confirm_password="mypassword"
)
print(user.json())
# '{"username": "Vinod", "email": "vinod@example.com", "password": "mypassword", "confirm_password": "mypassword"}'
```

✅ **Interview Tip:**

* Always mention **custom validators** for fields that require **business logic** (password matching, age limit, username rules).
* Know **serialization techniques** (`.dict()`, `.json()`) as FastAPI uses these for API responses.