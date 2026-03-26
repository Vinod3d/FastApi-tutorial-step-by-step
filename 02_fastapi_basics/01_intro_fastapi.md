# Introduction to FastAPI

## What you will learn
- What FastAPI is and why it's so popular
- The core technologies backing FastAPI (Starlette & Pydantic)
- What makes FastAPI incredibly fast (ASGI)

## Concept (Simple Explanation)
FastAPI is a modern web framework for building APIs with Python. Think of a framework like a pre-built house frame—instead of building everything from scratch (handling HTTP requests, routing, data validation), FastAPI does the heavy lifting for you so you can just focus on decorating the rooms (writing your business logic).

It stands on the shoulders of two giants:
1. **Starlette:** Handles the web parts (routing, requests, ASGI).
2. **Pydantic:** Handles the data parts (validation, serialization).

## Code Example
There is no code for this conceptual intro, but this is the mental model you need:
```python
# A typical mental model of a FastAPI app
from fastapi import FastAPI
app = FastAPI()

# 1. Client sends Data -> 2. Pydantic Validates Data -> 3. Your Function Runs -> 4. FastAPI Returns JSON
```

## Best Practices
- **Embrace Type Hints:** FastAPI's superpower is built around standard Python type hints (`name: str`, `age: int`). If you don't use type hints, you lose 90% of FastAPI's benefits.
- **Learn Async:** To get the true performance of FastAPI, understand `async` and `await` deeply.

## Common Mistakes
- **Treating it like Flask/Django:** FastAPI uses ASGI (asynchronous), while Flask traditionally uses WSGI (synchronous). You can't just copy-paste Flask architectural patterns and expect them to be efficient in FastAPI.
- **Ignoring Pydantic:** Manual data validation (e.g., `if type(age) != int: return error`) is an anti-pattern in FastAPI. Always let Pydantic handle it.

## Interview Questions
**Q: What is FastAPI built on?**
A: It is built on Starlette for web routing/ASGI support, and Pydantic for data validation and serialization.

**Q: Why is FastAPI considered one of the fastest Python frameworks?**
A: Because it utilizes ASGI (Asynchronous Server Gateway Interface) natively, allowing it to handle thousands of concurrent requests natively without blocking, similar to NodeJS or Go.
