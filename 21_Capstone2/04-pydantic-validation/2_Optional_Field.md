

## Optional Fields, Default Values & Nested Models

### **1. Optional Fields**

* Sometimes, not all data is required.
* Use **`Optional`** from the `typing` module to define fields that may be **`None`**.

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]  # may or may not be provided
```

**Usage:**

```python
user1 = User(id=1, name="Vinod", email="vinod@example.com")
print(user1.phone)  # Output: None

user2 = User(id=2, name="Anita", email="anita@example.com", phone="9876543210")
print(user2.phone)  # Output: 9876543210
```

* ✅ **Interview Tip:** Explain that `Optional` doesn’t mean the field is optional in input—it means it can be `None`. For truly optional input, use **default values**.

### **2. Default Values**

* Default values make fields optional in input.
* If not provided, Pydantic uses the default.

```python
class User(BaseModel):
    id: int
    name: str
    is_active: bool = True
```

```python
user = User(id=1, name="Vinod")
print(user.is_active)  # True
```

* Can also use **default_factory** for dynamic defaults like lists, datetime, etc.

```python
from datetime import datetime
from pydantic import BaseModel, Field

class Event(BaseModel):
    name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

event = Event(name="FastAPI Class")
print(event.timestamp)  # Current UTC time
```

### **3. Nested Models**

* You can define models **inside models**, useful for structured data like JSON.

**Example:**

```python
class Address(BaseModel):
    city: str
    country: str

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Address  # Nested model
```

**Usage:**

```python
user = User(
    id=1,
    name="Vinod",
    email="vinod@example.com",
    address={"city": "Delhi", "country": "India"}
)
print(user)
# Output: id=1 name='Vinod' email='vinod@example.com' address=Address(city='Delhi', country='India')
```

* ✅ **Interview Tip:** Nested models are frequently asked:

  * Explain how Pydantic **auto-validates nested structures**.
  * Shows understanding of **JSON → Python object mapping**, which is critical in APIs.

### **4. Real-world Example: Users with Addresses**

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    address: Optional[Address]  # Optional nested field

# User with no address
user1 = User(id=101, name="Anita", email="anita@example.com")
# User with address
user2 = User(
    id=102,
    name="Raj",
    email="raj@example.com",
    address={"street": "MG Road", "city": "Mumbai", "country": "India"}
)
```