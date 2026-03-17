हाँ। अब तुम्हारे current files देखकर **पूरे next steps** साफ-साफ बता देता हूँ।

सबसे पहले, तुम्हारी files में **2 जरूरी corrections** हैं।

# पहले correction करो

## 1) Dockerfile में code copy नहीं हो रहा

तुम्हारे Dockerfile में यह missing है:

```dockerfile
COPY . .
```

अभी तुम्हारा Dockerfile सिर्फ `requirements.txt` copy कर रहा है, लेकिन **पूरा project code container में नहीं जा रहा**।
इसलिए `auth.main:app` run नहीं होगा।

## 2) MySQL password mismatch है

Compose file में:

```yaml
MYSQL_PASSWORD: root123
```

लेकिन db service में:

```yaml
MYSQL_ROOT_PASSWORD: root
```

यह mismatch है।

अगर backend root user से connect करेगी, तो दोनों side password same होना चाहिए।

---

# Final corrected files

## `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "auth.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## `docker-compose.yml`

अगर तुम्हारे system में 3306 busy हो सकता है, तो safe version यही है:

```yaml
services:
  backend:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      MYSQL_HOST: db
      MYSQL_PORT: 3306
      MYSQL_USER: root
      MYSQL_PASSWORD: root123
      MYSQL_DATABASE: fastapi_db

  db:
    image: mysql:8
    container_name: mysql_db
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: fastapi_db
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

volumes:
  mysql_data:
```

---

# अब पूरे steps

## Step 1: project structure check करो

तुम्हारा folder कुछ ऐसा होना चाहिए:

```text
21_Capstone2/
│
├── auth/
│   ├── main.py
│   ├── auth_database.py
│   ├── model.py
│   ├── utils.py
│   └── Schema.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .dockerignore
```

सबसे important:

* `auth` folder होना चाहिए
* `auth/main.py` होना चाहिए
* `main.py` में `app = FastAPI()` होना चाहिए

---

## Step 2: `.dockerignore` बनाओ

Project root में `.dockerignore` file बनाओ:

```txt
__pycache__/
*.pyc
*.pyo
*.pyd
.env
venv/
env/
myenv/
.git
.vscode/
.idea/
```

---

## Step 3: database code check करो

तुम्हारी Python DB config में host यही होना चाहिए:

```python
MYSQL_HOST = "db"
```

`localhost` नहीं होना चाहिए, क्योंकि Docker Compose में backend MySQL container को `db` नाम से access करेगी।

अगर env variables पढ़ रहे हो, तो और भी अच्छा।

---

## Step 4: old containers बंद करो

Terminal में:

```bash
docker compose down
```

अगर पुराने stopped containers भी हैं, तब भी ठीक है।

---

## Step 5: image build + containers start करो

अब चलाओ:

```bash
docker compose up --build -d
```

इस command से:

* backend image build होगी
* mysql image pull होगी
* db container start होगी
* db healthy होने के बाद backend start होगी

---

## Step 6: running containers check करो

```bash
docker ps
```

तुम्हें ideally यह दिखना चाहिए:

* `fastapi_app` → Up
* `mysql_db` → Up (healthy)

अगर backend नहीं चल रही, तो next step करो।

---

## Step 7: logs check करो

### backend logs

```bash
docker logs fastapi_app
```

### db logs

```bash
docker logs mysql_db
```

अगर कोई error होगी तो यहीं दिखेगी।

---

## Step 8: app browser में check करो

Open करो:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

अगर docs open हो गईं, तो Docker setup सही है।

---

## Step 9: MySQL host machine से access करनी हो तो

तुमने यह mapping रखी है:

```yaml
- "3307:3306"
```

इसका मतलब:

* laptop से connect करते समय host = `localhost`
* port = `3307`

लेकिन backend container के अंदर अब भी:

* host = `db`
* port = `3306`

---

# अब Docker Hub पर डालने के steps

जब local run सही हो जाए, उसके बाद push करो।

## Step 10: local image names देखो

```bash
docker images
```

तुम्हें कुछ ऐसा दिख सकता है:

* `21_capstone2-backend`
* या कोई compose-generated image name

अगर तुम clear नाम चाहते हो, तो compose के बजाय अलग से image build करना आसान है।

---

## Step 11: direct clean image build करो

यह command चलाओ:

```bash
docker build -t fastapi-auth-app .
```

अब तुम्हारे पास एक साफ local image होगी:

* `fastapi-auth-app:latest`

---

## Step 12: Docker Hub login करो

```bash
docker login
```

अपना Docker Hub username/password डालो।

---

## Step 13: Docker Hub format में tag करो

मान लो तुम्हारा Docker Hub username है `vinodchandra`

तो:

```bash
docker tag fastapi-auth-app vinodchandra/fastapi-auth-app:latest
```

---

## Step 14: push करो

```bash
docker push vinodchandra/fastapi-auth-app:latest
```

बस, अब image Docker Hub पर upload हो जाएगी।

---

## Step 15: Docker Hub site पर check करो

अपने account में repository section में image दिखेगी:

```text
vinodchandra/fastapi-auth-app
```

---

# पूरा command flow

यह पूरा exact flow है:

```bash
docker compose down
docker compose up --build -d
docker ps
docker logs fastapi_app
docker logs mysql_db
docker build -t fastapi-auth-app .
docker login
docker tag fastapi-auth-app vinodchandra/fastapi-auth-app:latest
docker push vinodchandra/fastapi-auth-app:latest
```

---

# Important mistakes jo avoid karni hain

## 1. `COPY . .` भूलना

इससे code container में नहीं जाएगा।

## 2. Password mismatch

यह नहीं होना चाहिए:

* backend password = `root123`
* db root password = `root`

दोनों same रखो।

## 3. MySQL host `localhost` रखना

Compose setup में गलत है। `db` होना चाहिए।

## 4. Host port 3306 use करना जब local MySQL पहले से चल रही हो

इसलिए `3307:3306` safer है।

---

# Final summary

तुम्हारे लिए सही sequence यह है:

1. Dockerfile fix करो
2. docker-compose.yml fix करो
3. `.dockerignore` बनाओ
4. `docker compose up --build -d`
5. browser में `localhost:8000/docs` check करो
6. फिर `docker build -t fastapi-auth-app .`
7. `docker login`
8. `docker tag ...`
9. `docker push ...`

अगर चाहो, मैं अगले message में तुम्हारे लिए **exact final files** एकदम copy-paste format में दे दूँ:

* `Dockerfile`
* `docker-compose.yml`
* `.dockerignore`
* DB config snippet
* exact Docker Hub commands
