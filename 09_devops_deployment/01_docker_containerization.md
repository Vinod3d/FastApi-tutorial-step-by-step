# Dockerizing FastAPI

## What you will learn
- Why "It works on my machine" is unacceptable in production
- Writing a production-ready `Dockerfile`
- Utilizing `.dockerignore` to prevent security leaks
- Pushing your image to Docker Hub

## Concept (Simple Explanation)
When you write code on your Windows laptop and send it to an AWS Linux server, it often crashes because of different operating systems and mismatched Python versions.

**Docker** solves this by putting your code, Python 3.11, and all your requirements inside a virtual, self-contained box (a Container). If the box works on your laptop, Docker guarantees that the exact same box will work perfectly on AWS, Google Cloud, or your friend's Macbook.

## Code Example
**1. The `.dockerignore` file**
Never copy your virtual environment or `.env` secrets into the container!
```text
__pycache__/
*.pyc
.env
venv/
.git
```

**2. The Production `Dockerfile`**
```dockerfile
# 1. Use a lightweight official Python image
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy ONLY requirements first (Exploits Docker Cache for faster builds)
COPY requirements.txt .

# 5. Install dependencies without cache to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Expose the port FastAPI will run on
EXPOSE 8000

# 8. Start the FastAPI server using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Best Practices
- **Copy `requirements.txt` BEFORE the rest of your code:** Docker builds images in layers. If you change a single line in `main.py`, Docker will realize the `COPY requirements.txt` step hasn't changed, and it will skip reinstalling all your pip packages, saving you minutes of build time.

## Common Mistakes
- **Forgetting `COPY . .`:** A wildly common beginner mistake. It copies `requirements.txt`, installs them, and then tries to run Uvicorn without actually copying `main.py` into the container, causing a fatal "Module Not Found" error upon startup.
- **Using `--host 127.0.0.1` inside Docker:** If you tell Uvicorn to bind to localhost inside the container, nothing outside the container can ever reach it! You must use `--host 0.0.0.0` so it listens on all network interfaces.

## Interview Questions
**Q: Why do we use `python:3.11-slim` or `alpine` instead of just `python:3.11`?**
A: Standard Python images contain hundreds of megabytes of underlying OS utilities (compilers, build tools) that are completely unnecessary for simply running a web server. Using a `-slim` image massively reduces the final Docker image footprint from ~1GB down to ~150MB, saving money on server storage and decreasing deployment times.

**Q: Explain the flow of publishing a Docker Image.**
A: After writing the `Dockerfile`, you run `docker build -t myapp .` to build the local image. You then `docker login` to authenticate with a registry like Docker Hub or AWS ECR. You `docker tag` the image with your repository name, and finally `docker push username/myapp:latest` to upload it to the cloud.
