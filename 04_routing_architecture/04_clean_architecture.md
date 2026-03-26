# Clean Architecture & Design Patterns

## What you will learn
- The principles of Clean Architecture 
- Why we decouple the API layer from the Database layer
- Implementing the Service Layer Pattern
- Implementing the Repository Pattern

## Concept (Simple Explanation)
If a restaurant's waiter (the API router) has to take your order, go to the kitchen, chop the vegetables (business logic), cook the food (database operations), and then bring it to you, they will eventually drop a plate.

**Clean Architecture** means assigning strict roles.
- **Routers (Waiters):** Receive requests and return responses.
- **Services (Chefs):** Execute the core business logic (math, tax calculations, sending emails).
- **Repositories (Inventory managers):** Talk exclusively to the Database to fetch or save items.

If you change your database from PostgreSQL to MongoDB, only the Repository changes! The Services and Routers never even know it happened.

## Code Example
Instead of putting everything in `@app.post("/users")`:

**1. The Repository (Data Layer)**
```python
# db/repositories.py
class UserRepository:
    def __init__(self, db_session):
        self.db = db_session
        
    def save_user(self, user_data: dict):
        # The ONLY place where raw SQL/ORM code goes
        print(f"Saving {user_data} to Database...")
        return {"id": 1, **user_data}
```

**2. The Service (Business Logic Layer)**
```python
# services/user_service.py
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    def create_user(self, name: str):
        # The ONLY place where business rules go
        if name == "admin":
            raise ValueError("Admin is a reserved name")
            
        name = name.capitalize() # Business logic modification
        return self.repo.save_user({"name": name})
```

**3. The Router (Web Layer)**
```python
# api/routers.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/users")
async def create_new_user(name: str):
    # The Router does no math and no database queries. It just orchestrates!
    repo = UserRepository(db_session="fake_db")
    service = UserService(repo)
    
    try:
        new_user = service.create_user(name)
        return {"result": new_user}
    except ValueError as e:
        return {"error": str(e)}
```

## Best Practices
- **Never import FastAPI in your Service or Repository:** Your business logic should be entirely decoupled from the HTTP framework. If you copy/paste your `UserService` into a random Python script or a background worker (like Celery), it should run perfectly without knowing what a webservice is.
- **Inject Repositories into Services:** This makes writing Unit Tests incredibly easy. You can pass a "Fake/Mock" repository into the service during testing so you don't actually hit a real database.

## Common Mistakes
- **The "Fat" Router anti-pattern:** Writing hundreds of lines of complex database joins and data transformations directly inside an `@app.get()` decorator.
- **Over-engineering:** Clean Architecture is fantastic for large projects. For a simple microservice with exactly two endpoints that just read a database, full Clean Architecture might be overkill. Balance is key.

## Interview Questions
**Q: What is the Repository Pattern?**
A: It is a design pattern that abstracts data access. It acts as an intermediary collection interface, hiding the complex database querying logic from the rest of the application.

**Q: In Clean Architecture, why shouldn't the Service Layer return HTTPExceptions?**
A: Because the Service Layer should not know about HTTP concepts. It should raise standard Python Exceptions (like `ValueError` or custom domain exceptions). The Web Layer (FastAPI Routers or Exception Handlers) should catch those domain exceptions and translate them into `HTTPExceptions` (`400`, `404`, etc) to return to the client.
