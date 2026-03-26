# Server Architecture: Uvicorn & Gunicorn

## What you will learn
- Understanding ASGI Servers (Uvicorn)
- Scaling vertically with Process Managers (Gunicorn)
- Preventing application bottlenecks under heavy traffic
- The standard command to run FastAPI in production

## Concept (Simple Explanation)
**Uvicorn** is an incredibly fast, asynchronous worker. But a single Uvicorn worker can only use a single CPU core. If your AWS server has 8 CPU cores, standard Uvicorn will leave 7 of them completely asleep.

**Gunicorn** is a Manager. It doesn't actually run your FastAPI code. Instead, it looks at your server, says "Ah, 8 CPU cores!", and spawns 8 separate Uvicorn workers. It sits at the front door, receives all internet traffic, and efficiently distributes the requests among the 8 workers to maximize throughput.

## Code Example
**Running in Development (Single Worker)**
```bash
uvicorn app.main:app --reload
```
*Never use `--reload` in production. It wastes massive amounts of memory scanning files for changes.*

**Running in Production (Multiple Workers)**
To install Gunicorn with the Uvicorn worker class:
```bash
pip install gunicorn uvicorn[standard]
```

Run the application:
```bash
# -w 4 means "start 4 worker processes"
# -k uvicorn.workers.UvicornWorker tells Gunicorn to use Uvicorn for the underlying work
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Best Practices
- **Tuning your Workers:** The industry standard formula for Gunicorn workers is `(2 x CPU Cores) + 1`. If your server has 4 CPUs, you should run `gunicorn -w 9`. This ensures that if some workers are waiting on a slow database query, other workers are still available to handle new requests.
- **Behind a Reverse Proxy:** In a true production environment, Gunicorn shouldn't be directly exposed to the internet. Traffic should hit an NGINX or Caddy server first (which handles HTTPS/SSL and static files), which then internally forwards the dynamic API requests to Gunicorn.

## Common Mistakes
- **Running raw `uvicorn` in production:** Relying purely on Uvicorn without a process manager means if your single Uvicorn process encounters an unhandled fatal error and crashes, your entire API goes down instantly. Gunicorn automatically detects crashed workers and respawns them immediately, guaranteeing high availability.

## Interview Questions
**Q: Explain the difference between WSGI and ASGI.**
A: WSGI (Web Server Gateway Interface) is the synchronous Python standard used by older frameworks like Django and Flask. It handles one request at a time sequentially per worker thread. ASGI (Asynchronous Server Gateway Interface) is the modern standard used by FastAPI. It supports asynchronous `async/await` execution, allowing a single worker to pause an I/O bound request (like a DB query) and instantly serve hundreds of other requests concurrently.

**Q: Why don't we use standard Gunicorn workers for FastAPI?**
A: Standard Gunicorn workers are designed for WSGI (synchronous applications). Since FastAPI is inherently ASGI, sending tasks to standard Gunicorn workers would strip away all of FastAPI's async speed benefits. We must explicitly specify `-k uvicorn.workers.UvicornWorker` to preserve the async runtime.
