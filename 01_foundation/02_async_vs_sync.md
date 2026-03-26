# Async vs Sync Programming

## What you will learn
- The difference between Synchronous and Asynchronous execution
- How the Event Loop works
- When to use `async` / `await` in FastAPI
- The difference between Blocking and Non-Blocking code

## Concept (Simple Explanation)
Imagine you are a chef in a restaurant. 
- **Synchronous (Sync):** You put a pizza in the oven and stare at it for 15 minutes until it's done. You do nothing else. (Blocking)
- **Asynchronous (Async):** You put the pizza in the oven, set a timer, and go chop onions for another dish. When the timer rings, you take the pizza out. (Non-blocking)

FastAPI is incredibly fast because it acts like an "asynchronous chef" using an Event Loop to juggle thousands of requests without waiting idly.

## Code Example
```python
import asyncio
import time

# --- SYNCHRONOUS (Blocking) ---
def sync_task():
    print("Starting sync task...")
    time.sleep(2) # Blocks the entire program
    print("Finished sync task!")

# --- ASYNCHRONOUS (Non-Blocking) ---
async def async_database_call():
    print("Making async DB call...")
    await asyncio.sleep(2) # Gives control back to the event loop!
    print("Got data from DB!")

async def main():
    # Running multiple async tasks concurrently
    print("Starting async tasks...")
    await asyncio.gather(
        async_database_call(),
        async_database_call()
    )

# To run the async code in standard Python script (outside FastAPI):
# asyncio.run(main())
```

## Best Practices
- **Never mix sync blocking calls inside async functions:** If you use `time.sleep()` or a synchronous database driver (like standard `psycopg2`) inside an `async def` route, it acts like a traffic jam and blocks the *entire* server.
- **Use `async def` for I/O operations:** Always use it when calling external APIs, databases, or reading files.
- **Use `def` for CPU-heavy tasks:** If a route does heavy math, declare it as a standard `def` so FastAPI can run it in an external threadpool without blocking the main event loop.

## Common Mistakes
- **Forgetting to `await`:** Calling `async_database_call()` without `await` won't run the function; it just returns an unexecuted coroutine object.
- **Using `time.sleep()` in FastAPI:** This is a lethal mistake for API performance. Always use `asyncio.sleep()` if you need a delay, or use async native libraries.

## Interview Questions
**Q: What is the difference between concurrency and parallelism?**
A: Concurrency is managing multiple tasks at once (like one chef switching between cooking pasta and chopping veggies). Parallelism is executing multiple tasks physically at the exact same time (like two distinct chefs working side-by-side on two CPUs).

**Q: What is an Event Loop?**
A: It is the core engine of asynchronous programming. It constantly checks for and schedules pending tasks, shifting execution away from tasks that are waiting for I/O operations.

**Q: Why is FastAPI faster than Flask or Django natively?**
A: FastApi uses ASGI (Asynchronous Server Gateway Interface) natively, allowing it to handle thousands of concurrent I/O-bound requests without waiting for one to finish before starting the next.
