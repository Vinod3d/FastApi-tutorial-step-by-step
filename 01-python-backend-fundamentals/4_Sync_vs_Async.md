

# 🚀 Chapter 1.4 Sync vs Async Programming


## 1. What is Synchronous Programming?

In synchronous execution:

* One task runs at a time
* Next task waits until previous finishes
* Blocking behavior

Example:

```python
import time

def task():
    time.sleep(3)
    print("Done")

task()
```

Here:

* Program waits 3 seconds
* Nothing else runs

This is blocking.


## 2. What is Asynchronous Programming?

Asynchronous means:

* Multiple tasks can run concurrently
* While waiting, program can execute other tasks
* Non-blocking

Example:

```python
import asyncio

async def task():
    await asyncio.sleep(3)
    print("Done")

asyncio.run(task())
```

Here:

* Instead of blocking
* It gives control back to event loop


## 3. Blocking vs Non-Blocking

### Blocking

Program waits and does nothing else.

Example:

* time.sleep()
* Database call (sync)
* API call (sync)

### Non-Blocking

Program can switch to other tasks while waiting.

Example:

* await asyncio.sleep()
* async database calls

---

## 4. Concurrency vs Parallelism 

### Concurrency

Multiple tasks progress together
Single CPU can manage by switching tasks.

### Parallelism

Multiple tasks run at same time
Requires multiple CPUs.


### Simple Difference:

Concurrency → Managing multiple tasks
Parallelism → Executing multiple tasks physically at same time

FastAPI uses concurrency.


## 5. What is async and await?

### async

Marks function as asynchronous.

```python
async def fetch():
    pass
```

### await

Pauses function until awaited task completes.

```python
await asyncio.sleep(2)
```

Important:
You can only use await inside async function.

## 6. What is Event Loop?

Event loop is:

* The core engine of async programming
* It schedules tasks
* It switches between tasks when one is waiting

Think of it like:

A manager controlling multiple workers efficiently.

In Python:

```python
asyncio.run(main())
```

Starts event loop.

## 7. How Async Works Internally

When async function hits:

```python
await some_task()
```

It:

1. Suspends current function
2. Returns control to event loop
3. Event loop runs another task
4. When task completes → resumes original function

This makes program efficient.

## 8. Why FastAPI is Fast?

FastAPI uses:

* ASGI (Asynchronous Server Gateway Interface)
* async functions
* Non-blocking I/O

Traditional frameworks like Flask use WSGI (sync).

FastAPI can handle thousands of concurrent requests.


## 9. When to Use async in FastAPI?

Use async when:

* Calling external API
* Calling database asynchronously
* File I/O operations
* Network operations

Do NOT use async for:

* Heavy CPU operations
* Simple calculations


## 📌 10. Common Interview Questions

1. Difference between sync and async?
2. What is blocking?
3. What is non-blocking?
4. What is event loop?
5. What is concurrency vs parallelism?
6. Why FastAPI is faster than Flask?
7. What happens when await is used?
8. Can we use await in normal function?

You must explain confidently.


## 11. Common Beginner Mistake

Wrong:

```python
async def test():
    time.sleep(5)
```

Correct:

```python
async def test():
    await asyncio.sleep(5)
```

If you use time.sleep() → it blocks event loop.

## 12. ASGI vs WSGI

WSGI:

* Synchronous
* One request at a time per worker

ASGI:

* Asynchronous
* Supports WebSockets
* Supports long-lived connections

FastAPI uses ASGI.