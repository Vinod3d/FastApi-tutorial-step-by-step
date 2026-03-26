# Background Tasks

## What you will learn
- How to return API responses instantly while heavy processing continues
- Utilizing FastAPI's native `BackgroundTasks`
- When to use standard BackgroundTasks vs Celery/Redis
- Real-world Notification / Email sending examples

## Concept (Simple Explanation)
Imagine you order a coffee. The barista takes your order, hands you a receipt, and says "It will be ready in 5 minutes" (Instantly returning the API Response). You go sit down. Meanwhile, the barista starts actually grinding the beans and making the coffee in the background.

If you sign up for a website, the server has to send you a Welcome Email. Sending an email takes 3 seconds. The user shouldn't stare at a loading spinner for 3 seconds. You should return "Account Created!" instantly, and trigger the email to send *in the background*.

## Code Example
**1. Simple Background Task**
```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# 1. This is a standard Python function. It can be async or sync.
def write_welcome_log(email: str, message: str):
    with open("log.txt", mode="a") as email_file:
        email_file.write(f"Email sent to {email}: {message}\n")

@app.post("/register")
async def register_user(email: str, background_tasks: BackgroundTasks):
    
    # Simulate DB Save
    user_id = 101 
    
    # 2. Add the function and its arguments to the task queue.
    # Note: We pass the function reference `write_welcome_log`, we do NOT invoke it `()` here!
    background_tasks.add_task(write_welcome_log, email, "Welcome to the Platform!")
    
    # 3. This return statement executes instantly. The user sees this IMMEDIATELY.
    # The background task fires only *after* this response is fully sent.
    return {"message": "User registered successfully! Check your email."}
```

## Best Practices
- **Use `BackgroundTasks` for lightweight operations:** Sending a simple confirmation email, writing a file to AWS S3, or updating a cache metric are perfect. 
- **Use Celery/Redis for heavyweight operations:** If you need to transcode a 4K Video (which takes 2 hours), do not use FastAPI's `BackgroundTasks`. It runs in the exact same memory space as your API. If the server crashes, the task is lost forever. Use a distributed task queue like Celery or RQ for critical, heavy jobs.

## Common Mistakes
- **Putting CPU-Heavy work in sync tasks:** If you write a `def compute_pi():` sync function and put it in a background task, because Python has a Global Interpreter Lock (GIL), the heavy math will actually freeze your entire FastAPI server while it runs in the background.
- **Accidentally calling the function in `add_task`:** 
  - BAD: `background_tasks.add_task(send_email())` -> This executes it instantly, defeating the purpose!
  - GOOD: `background_tasks.add_task(send_email, "user@gmail.com")`

## Interview Questions
**Q: How does FastAPI's BackgroundTask differ from Python threading?**
A: FastAPI's `BackgroundTasks` is built directly into Starlette. It ensures that the background execution only begins *after* the HTTP response has been completely sent over the wire to the client. Normal Python threading might execute simultaneously, wasting CPU while the response is still trying to formulate.

**Q: If my FastAPI server restarts dynamically (via Kubernetes or Heroku), what happens to my active BackgroundTasks?**
A: They are instantly destroyed and lost forever. Standard `BackgroundTasks` are stored entirely in RAM memory. For guaranteed delivery and retry mechanics, you must implement a robust message broker like RabbitMQ or Redis with Celery.
