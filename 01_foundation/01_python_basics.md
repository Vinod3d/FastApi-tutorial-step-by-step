# Python Basics for FastAPI

## What you will learn
- Core Python concepts essential for backend development
- Dynamic typing vs Type Hinting (crucial for FastAPI)
- Data structures and when to use them
- How `*args` and `**kwargs` work in real applications

## Concept (Simple Explanation)
Python is a dynamically typed, high-level language. Think of variable creation in Python like putting labels on boxes; you don't need to declare what goes in the box beforehand, you just put the item in and label it. However, in modern FastAPI, we add "Type Hints" (like saying "this box only accepts integers") to make our code production-ready and error-free.

## Code Example
```python
from typing import List, Dict

# 1. Type Hinting (Crucial for FastAPI and Pydantic)
def get_user(user_id: int) -> Dict[str, str]:
    # user_id must be an integer, returns a dictionary
    return {"id": str(user_id), "name": "Vinod", "role": "admin"}

# 2. *args and **kwargs (Used in decorators and dependency injection)
def process_request(*args, **kwargs):
    print(f"Positional args (Tuple): {args}")
    print(f"Keyword args (Dict): {kwargs}")

# 3. List Comprehension (Fast and Pythonic)
def get_active_users(users: List[Dict]) -> List[Dict]:
    return [user for user in users if user.get("is_active")]

# Test the functions
print(get_user(101))
process_request("GET", "/users", auth_token="abc123yz")
```

## Best Practices
- **Always use Type Hints:** Even though Python doesn't enforce them at runtime, FastAPI relies heavily on type hints to validate data, map inputs, and generate interactive documentation.
- **Use List Comprehensions:** They are faster and more readable than `for` loops with `append()`.
- **Avoid Global Variables:** They make debugging difficult and can cause race conditions in concurrent web requests.

## Common Mistakes
- **Mutating Default Arguments:** Using a mutable object (like a list `[]` or dict `{}`) as a default argument. It retains its state across API calls! *Always use `None` as the default instead.*
- **Confusing `is` and `==`:** `==` checks if the *values* are the same. `is` checks if they are the exact same *object in memory*.

## Interview Questions
**Q: What is the difference between a list and a tuple?**
A: A list is mutable (can be changed), while a tuple is immutable (cannot be changed after creation). Tuples are slightly faster and used for fixed data.

**Q: Why do we use `*args` and `**kwargs`?**
A: They allow a function to accept a variable number of positional (`*args`) and keyword (`**kwargs`) arguments, making functions flexible. This is heavily used when writing wrappers or decorators in application frameworks.

**Q: Explain dynamic typing in Python.**
A: In Python, you don't need to declare a variable's type explicitly. The type is determined at runtime based on the value assigned to it.
