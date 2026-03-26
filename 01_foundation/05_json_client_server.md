# JSON & Client-Server Architecture

## What you will learn
- Why JSON is the industry standard for APIs
- Serialization vs Deserialization
- How Pydantic solves JSON validation in FastAPI
- The complete Client-Server flow

## Concept (Simple Explanation)
**Client-Server:** Imagine a drive-thru. You in your car is the **Client** (the frontend or mobile app). The person taking your order inside the building is the **Server** (FastAPI backend). 
**JSON:** The language you both speak is **JSON**. It's just a standardized format for writing down data so both the Client and Server can perfectly understand each other without confusion. 

**Serialization** is translating your thoughts into spoken words (Python object -> JSON string).
**Deserialization** is the server hearing your words and understanding the concept (JSON string -> Python object).

## Code Example
```python
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# 1. Pydantic Model handles Deserialization AND Validation automatically
class UserCreate(BaseModel):
    name: str
    age: int
    skills: list[str]

@app.post("/users")
async def create_user(user: UserCreate):
    # 'user' is now a validated Python object!
    print(f"Creating user {user.name} who knows {user.skills}")
    
    # 2. FastAPI automatically handles Serialization for the response
    return {"status": "success", "data": user.model_dump()}

# --- Standard Python JSON without FastAPI (For understanding) ---
# Serialization (Dict -> String)
data = {"name": "Vinod", "age": 25}
json_string = json.dumps(data)

# Deserialization (String -> Dict)
parsed_dict = json.loads(json_string)
```

## Best Practices
- **Use Pydantic:** Never parse raw JSON strings manually using `json.loads()` inside FastAPI routes. Always declare a Pydantic `BaseModel` and let FastAPI automatically parse, type-cast, and validate the body for you.
- **Microservices over Monoliths:** As systems grow, split your single monolithic backend server into multiple smaller services (e.g., Auth Service, Payment Service) that communicate via APIs.

## Common Mistakes
- **Assuming JSON is a Python Dictionary:** They look similar, but JSON is a *string* format used for text transmission. A Python dict is a functional data structure in memory.
- **Not handling `datetime` serialization:** Standard `json.dumps()` will crash if you try to serialize a Python `datetime` object. Pydantic and FastAPI handle this automatically!

## Interview Questions
**Q: Explain the flow of a modern 3-Tier Architecture.**
A: 
1. **Presentation Layer (Frontend):** The React/Mobile app where the user clicks a button.
2. **Application Layer (Backend):** The FastAPI server that receives the HTTP request and handles business logic.
3. **Data Layer (Database):** PostgreSQL/MySQL where the data is actually stored.

**Q: What is Serialization and Deserialization?**
A: Serialization is converting an in-memory object (like a Python dictionary) into a transmittable format (like a JSON string). Deserialization is the reverse process: taking a JSON string and parsing it back into a native application object.

**Q: What is a Load Balancer?**
A: As traffic increases, a single server cannot handle all requests. A Load Balancer sits between the clients and the servers, distributing incoming traffic across multiple backend servers horizontally.
