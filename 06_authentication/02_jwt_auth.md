# JSON Web Tokens (JWT)

## What you will learn
- What a JWT is and why modern APIs use it over Session Cookies
- The three parts of a JWT (Header, Payload, Signature)
- How JWT enables "Stateless" authentication
- The security benefits and risks of JWTs

## Concept (Simple Explanation)
Traditionally, when you log into a website, the server creates a "Session ID", gives it to your browser, and saves a copy in its own memory. Every time you click a page, the server checks its memory to see if your ID is valid. This uses a lot of server memory.

A **JWT** is like a cryptographic passport. When you log in, the server gives you a passport that says: *"Name: Vinod, Role: Admin, Expires: Tomorrow."* The server signs it with a secret, invisible ink (Digital Signature) and gives it to you. The server *does not save it*. When you make a request, you show the passport. The server checks the invisible ink; if the ink is real, it trusts the passport without checking a database! This is called **Stateless Authentication**.

## Structure of a JWT
If you look at a raw JWT, it looks like gibberish:
`eyJhbGciOiJIUzI1Ni... . eyJ1c2VyX2lkIj... . SflKxwRJSMeKKF2Q...`

It consists of three parts separated by dots (`.`):
1. **Header:** Determines the hashing algorithm (usually HS256).
2. **Payload (Claims):** The actual JSON data (e.g., `{"user_id": 1, "role": "admin"}`). **This is readable by anyone! Never put passwords here!**
3. **Signature:** A cryptographic hash created by combining the Header, Payload, and your server's `SECRET_KEY`. If a hacker modifies the payload (changing their role from "user" to "admin"), the signature will instantly become invalid.

## Installation
To generate and verify JWTs safely in Python, you need the `PyJWT` library.

```bash
pip install PyJWT
```

## Code Example
**How a JWT is passed in a FastAPI HTTP Request:**
```text
GET /secure-dashboard HTTP/1.1
Host: api.myapp.com
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

**Generating a Token (Conceptual):**
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super_secret_string"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Expiration Claim
    
    # Encodes the JSON into a secure string using the Secret Key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

## Best Practices
- **Keep lifetimes short:** Access tokens should expire very quickly (e.g., 15 minutes). If a hacker steals a JWT, they possess it forever until it expires, because the server is stateless and cannot easily "revoke" a single JWT without complex blacklists.
- **Protect your SECRET_KEY:** If your secret key is leaked, attackers can forge JWTs and give themselves Admin access. Load it from a `.env` file!

## Common Mistakes
- **Storing sensitive data in the Payload:** The payload is merely Base64 encoded, not encrypted. Anyone who steals the token can paste it into `jwt.io` and read the JSON. Do not put emails, phone numbers, or passwords inside a JWT payload!

## Interview Questions
**Q: What makes JWT stateless, and why is that good for scalability?**
A: JWT is stateless because the server does not need to store active sessions in its memory or database. All validation data is contained entirely within the token's cryptographic signature. This makes microservices highly scalable because any server holding the Secret Key can validate the token without asking a central database.

**Q: Can you encrypt data inside a JWT?**
A: Standard JWTs only sign data, they do not encrypt it (the payload is readable). If encryption is required so the client cannot read the payload, you must use JWE (JSON Web Encryption), which is a different standard.
