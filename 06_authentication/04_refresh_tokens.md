# Refresh Tokens

## What you will learn
- Why access tokens must expire quickly
- What a Refresh Token is and how it replaces forced logins
- The architecture of a Dual-Token Flow
- Security best practices regarding token revocation

## Concept (Simple Explanation)
If an Access Token is a hotel guest's room key (JWT), it should expire fast—say, in 15 minutes. If it's stolen, the thief only has 15 minutes to exploit it. But making the real guest go to the front desk and log in every 15 minutes is terrible user experience.

The solution is the **Refresh Token**. It is a specialized, long-lived token (e.g., 7 days) given to the guest. It cannot open doors. Its *only* purpose is to be presented to the front desk when the main room key expires, proving identity quietly in the background to seamlessly receive a brand new 15-minute room key. 

## Code Example
**1. Providing two tokens at Login**
```python
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "my_secret"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    # Short lifespan (15 minutes)
    expire = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode({**data, "exp": expire, "type": "access"}, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    # Long lifespan (7 days)
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({**data, "exp": expire, "type": "refresh"}, SECRET_KEY, algorithm=ALGORITHM)

# In the login route:
# return {
#     "access_token": create_access_token({"sub": user.username}),
#     "refresh_token": create_refresh_token({"sub": user.username}),
# }
```

**2. The Refresh Endpoint**
```python
from fastapi import APIRouter, HTTPException

@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Security check: Ensure they didn't pass an expired access token instead!
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        username = payload.get("sub")
        
        # Issue a new access token
        new_access_token = create_access_token({"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired. Please log in again.")
```

## Best Practices
- **Store Refresh Tokens in HttpOnly Cookies:** Because refresh tokens have immense power (they can mint infinite access tokens), storing them in frontend LocalStorage exposes them to XSS attacks. Store them in secure, HttpOnly, SameSite cookies.
- **Implement Refresh Token Rotation:** Every time the client uses a refresh token to get a new access token, invalidate the old refresh token and issue a completely new one.

## Common Mistakes
- **Allowing an Access Token to be used as a Refresh Token:** A compromised access token should not be able to extend its own life. Always verify the token's type inside your `/refresh` endpoint logic!

## Interview Questions
**Q: Why don't we just make the Access Token last for 7 days?**
A: Because JWTs are stateless. If a bad actor steals an access token, the server cannot easily revoke it without introducing complex database blacklists (which ruins the performance benefit of JWT). By keeping access tokens short-lived (15m), the damage window is tiny. The long-lived refresh token can act as a targeted revocation tool.
