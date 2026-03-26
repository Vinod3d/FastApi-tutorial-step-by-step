# Role-Based Access Control (RBAC)

## What you will learn
- Embedding Roles inside JWT payloads
- Building dynamic FastAPI Dependencies for Authorization
- Creating clean, readable route protections
- Scaling permissions from simple apps to enterprise platforms

## Concept (Simple Explanation)
At a movie theater, the ticket (JWT) proves you are a paying customer (Authentication). However, depending on the role printed on the ticket—"Standard", "VIP", or "Employee"—the security guards will allow you into different areas (Authorization).

**Role-Based Access Control (RBAC)** assigns permissions rigidly to Roles, and assigns Users to Roles. This is massively superior to assigning 50 individual permissions to 500 individual users.

## Code Example
**1. Put the Role in the Token during Login**
```python
# During the login endpoint process:
# payload = {"sub": user.username, "role": user.role} # e.g., "admin", "customer"
# jwt.encode(payload, SECRET_KEY)
```

**2. Create a generic Dependency that fetches the User from the Token**
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Simulating database
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
    # In reality, fetch the user from Database to ensure they aren't deleted!
    return {"username": payload.get("sub"), "role": payload.get("role")}
```

**3. Create the RBAC Dependency Factory**
```python
def require_role(required_role: str):
    # This is a closure that returns a dependency function
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=403, 
                detail=f"Operation not permitted. Requires {required_role} privileges."
            )
        return current_user
    return role_checker
```

**4. Protect the Routes cleanly**
```python
from fastapi import APIRouter

router = APIRouter()

# Super clean: The router explicitly declares it demands an admin!
@router.delete("/users/{user_id}")
def delete_user(user_id: int, user: dict = Depends(require_role("admin"))):
    return {"message": f"User {user_id} deleted by Admin {user['username']}"}
```

## Best Practices
- **Consider Permission-Based Access Control at scale:** If your app grows massive, roles become messy (e.g., `admin`, `super_admin`, `billing_admin`). Switch to decoding specific granular scopes/permissions inside the token instead of broad roles.
- **Fetch the User from the DB:** While you *can* trust the role placed inside the JWT, best security practice usually involves taking the `user_id` from the JWT and pulling the latest Role status from the database. This ensures that if an Admin is demoted to a User, they lose access instantly, rather than retaining it until their JWT expires.

## Common Mistakes
- **Putting the RBAC logic inside the Route Body:**
  ```python
  # BAD - Litters the business logic
  @app.get("/data")
  def get_data(user=Depends(get_current_user)):
      if user.role != "admin": raise HTTPException(...)
      return data
  ```
  Always use FastAPI Dependencies so the route body focuses strictly on execution.

## Interview Questions
**Q: What is the main structural advantage of Role-Based Access Control (RBAC)?**
A: Separation of concerns and administrative scaling. By grouping permissions into Roles rather than attaching them directly to Users, when a company hires 10 new support agents, they simply assign them the "Support" role, rather than manually applying 30 disparate permissions to 10 separate user profiles.

**Q: In FastAPI, how can dependencies help implement RBAC gracefully?**
A: FastAPI allows dependencies to call other dependencies. We can chain a dependency flow: `OAuth2Bearer` extracts the token $\rightarrow$ `get_current_user` extracts the user data $\rightarrow$ `require_role_factory` checks the authorization. The final route only needs a single `Depends()` argument, resulting in immaculate code.
