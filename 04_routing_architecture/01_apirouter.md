# APIRouter & Route Ordering

## What you will learn
- Why you shouldn't put all routes in `main.py`
- How to group and structure endpoints using `APIRouter`
- Using `prefix` and `tags` for cleaner documentation
- Understanding why Route Ordering is critical in FastAPI

## Concept (Simple Explanation)
Imagine trying to run an entire hospital using one giant waiting room. It would be chaos! Instead, hospitals use **departments**: Cardiology, Neurology, Pediatrics.

In FastAPI, if you put 100 endpoints in `main.py`, it becomes unreadable. **APIRouter** is how we create "departments". You define groups of related routes in separate files, and then simply plug them into the main application. 

Additionally, we must understand **Route Ordering**. The receptionist always checks the directory from top to bottom. If your routes overlap, the first one found wins!

## Code Example
Instead of writing everything in `main.py`:

**1. Create a router file (`routers/users.py`)**
```python
from fastapi import APIRouter

# Initialize the router with a prefix and tag
router = APIRouter(prefix="/users", tags=["Users"])

# Static route MUST come before dynamic routes!
@router.get("/me")
async def get_current_user():
    return {"message": "You are the current administrative user."}

# Dynamic route
@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    return {"message": f"Fetching user {user_id}"}
```

**2. Plug it into `main.py`**
```python
from fastapi import FastAPI
from routers.users import router as users_router

app = FastAPI()

# Mount the router to the main app
app.include_router(users_router)
```

## Best Practices
- **Never put dynamic routes before static ones:** If `@router.get("/{user_id}")` is defined *above* `@router.get("/me")`, then visiting `/users/me` will try to find a user with the ID "me", causing a crash! Always define static fixed routes (`/me`, `/settings`) first.
- **Use `tags` aggressively:** The `tags=["Users"]` parameter automatically groups these endpoints together visually in the Swagger UI (`/docs`), making your API infinitely easier for front-end developers to read.

## Common Mistakes
- **Forgetting the leading slash:** Writing `prefix="users"` instead of `prefix="/users"` will break your routing completely.
- **Not importing the router correctly:** Be careful to import the actual `router` instance from the file, not the file module itself.

## Interview Questions
**Q: How does FastAPI resolve incoming HTTP requests against your route definitions?**
A: FastAPI (via Starlette) evaluates routes strictly from top to bottom in the order they were defined. The first route that matches both the HTTP method and the path structure is executed.

**Q: What is the purpose of APIRouter?**
A: `APIRouter` allows building modular, multi-file applications. It lets developers split huge applications into smaller, focused components, making the codebase scalable and maintainable.
