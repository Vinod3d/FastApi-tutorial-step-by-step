# HTTP Protocol Fundamentals

## What you will learn
- The role of HTTP in client-server communication
- Anatomy of an HTTP Request and Response
- Query Parameters vs Path Parameters
- Understanding HTTP Status Codes (Crucial for FastAPI)

## Concept (Simple Explanation)
HTTP (HyperText Transfer Protocol) is the language that the internet uses to talk. Imagine it like sending a formal letter through the mail.
- **The Client (You):** Writes a letter (Request), puts it in an envelope, writes the address (URL), and drops it in the mailbox.
- **The Server (FastAPI):** Receives the letter, reads the instructions, gathers the requested items, packages them up, and mails them back with a status note (Response).

## Code Example
```python
from fastapi import FastAPI, Response, status

app = FastAPI()

# 1. Path Parameter (Part of the URL path itself)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"message": f"Fetching data for user {user_id}"}


# 2. Query Parameter (Added after the ? in the URL)
# Example: /search?keyword=python&limit=10
@app.get("/search")
async def search_items(keyword: str, limit: int = 10):
    return {"searched": keyword, "returned": limit}


# 3. Setting HTTP Status Codes
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item():
    return {"message": "Item successfully created!"}
```

## Best Practices
- **Use the correct HTTP Method:** Don't use `POST` to fetch data, and don't use `GET` to insert data.
- **Return proper Status Codes:** FastAPI defaults to `200 OK`. If you create a resource, explicitly return `201 Created`. If something isn't found, raise a `404 Not Found` exception.
- **Handle CORS (Cross-Origin Resource Sharing):** In production, your frontend (`localhost:3000`) and backend (`localhost:8000`) run on different ports. Use FastAPI's `CORSMiddleware` to allow them to communicate.

## Common Mistakes
- **Mixing up Path and Query Parameters:** Remember: `users/1` is a path parameter (identifies a specific resource). `users?role=admin` is a query parameter (filters or modifies a list).
- **Ignoring Headers:** Trying to send JSON without setting `Content-Type: application/json` will result in the server failing to parse the body.

## Interview Questions
**Q: What is the difference between a Path Parameter and a Query Parameter?**
A: A path parameter is used to identify a specific resource (e.g., `/users/123`). A query parameter is used to filter, sort, or paginate a list of resources (e.g., `/users?role=admin`).

**Q: What does it mean that HTTP is "stateless"?**
A: It means the server does not remember anything from previous requests. Every request must contain all the necessary information (like an authentication token) to be understood and processed.

**Q: Explain the main categories of HTTP Status Codes.**
A: 2xx indicates Success (e.g., 200 OK, 201 Created). 4xx indicates a Client Error (e.g., 400 Bad Request, 404 Not Found). 5xx indicates a Server Error (e.g., 500 Internal Server Error).
