# Docker Compose & Multiple Containers

## What you will learn
- Why multi-container architectures are required in production
- Linking a FastAPI container to a MySQL container
- Managing Environment variables inside Docker networks
- Persisting database data using Docker Volumes

## Concept (Simple Explanation)
If Docker puts your FastAPI app in a box, what about your MySQL database? You shouldn't put them in the *same* box. If your app crashes, your database crashes.

Instead, you put FastAPI in one box, and MySQL in another box. **Docker Compose** is the manager that starts both boxes at the same time and creates an invisible bridge (a Docker Network) between them so they can talk to each other.

## Code Example
**`docker-compose.yml`**
```yaml
version: "3.8"

services:
  # 1. The FastAPI App Box
  backend:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy # Wait for MySQL to fully boot before starting FastAPI!
    environment:
      - MYSQL_HOST=db
      - MYSQL_PORT=3306
      - MYSQL_USER=root
      - MYSQL_PASSWORD=root123
      - MYSQL_DATABASE=fastapi_db

  # 2. The MySQL Database Box
  db:
    image: mysql:8
    container_name: mysql_db
    environment:
      - MYSQL_ROOT_PASSWORD=root123 # MUST MATCH THE BACKEND SETTING!
      - MYSQL_DATABASE=fastapi_db
    ports:
      - "3307:3306" # Maps your laptop's 3307 to the container's 3306
    volumes:
      - mysql_data:/var/lib/mysql # Protects data from being deleted
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

# 3. Docker Volumes
volumes:
  mysql_data:
```

## Best Practices
- **Use Database Volumes:** By default, when a Docker container is deleted (e.g., using `docker compose down`), all files inside it are annihilated. A Docker Volume (`mysql_data:/var...`) creates a safe folder on your server's physical hard drive to store the MySQL data permanently so it survives container restarts.
- **Use `depends_on` with `healthcheck`:** FastAPI starts in 1 second. MySQL takes 15 seconds to start. If FastAPI boots up and immediately tries to connect to the database, it will crash. Implementing a healthcheck forces FastAPI to patiently wait until MySQL is fully ready.

## Common Mistakes
- **Connecting to `localhost` inside Docker Compose:** Inside the backend container, `localhost` means the *FastAPI container itself*, not your laptop or the MySQL container. You must set `MYSQL_HOST=db` (the exact name of the service defined in the yaml file). Docker's internal DNS automatically routes "db" to the correct container IP.

## Interview Questions
**Q: How does networking work between containers inside a single Docker Compose file?**
A: Docker Compose automatically creates a default bridge network for the application. Every service defined in the file connects to this network and is given a DNS name identical to its service name (e.g., `db`, `backend`, `redis`). They can ping each other simply using those hostnames.

**Q: What does the port mapping `"3307:3306"` mean in Docker Compose?**
A: It maps Port 3307 on the physical Host computer (your laptop/server) to Port 3306 inside the Container. This allows you to securely expose containerized services to the outside world without forcing them to change their default internal binding configurations.
