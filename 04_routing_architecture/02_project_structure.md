# Production Project Structure

## What you will learn
- Why standardizing folder structures is critical
- A proven directory layout for production FastAPI apps
- Separation of concerns (Routers, Schemas, Models, Services)

## Concept (Simple Explanation)
If you throw all your clothes in a pile on the floor, getting dressed takes hours. If you use a closet with drawers for socks, shirts, and shoes, it takes seconds.

A **Project Structure** is the closet for your code. FastAPI doesn't force any structure on you (unlike Django). You can put everything in one file, but for a production app, this leads to disaster. You need to organize your code by its **purpose**.

## Code Example
Here is the industry-standard layout for a mid-to-large FastAPI project:

```text
my_fastapi_project/
├── app/
│   ├── main.py               # The entrypoint (FastAPI instance)
│   ├── api/                  # The Web Layer
│   │   ├── dependencies.py   # Auth checks, DB sessions
│   │   └── routers/          # APIRouters (users.py, items.py)
│   │
│   ├── core/                 # App-wide settings
│   │   ├── config.py         # Environment variables (Pydantic BaseSettings)
│   │   └── security.py       # Password hashing, JWT creation
│   │
│   ├── db/                   # Database Layer
│   │   ├── session.py        # SQLAlchemy engine and sessionmaker
│   │   └── models/           # SQLAlchemy DB Models (tables)
│   │
│   ├── schemas/              # Pydantic Models Layer
│   │   └── user_schema.py    # Request/Response validation
│   │
│   └── services/             # Business Logic Layer
│       └── user_service.py   # "Create user" logic, heavy lifting
│
├── tests/                    # Pytest test cases
├── requirements.txt          # Python dependencies
└── .env                      # Secrets (NEVER push to GitHub!)
```

## Best Practices
- **Separate DB instances from validation schemas:** Keep your SQLAlchemy (`models/`) completely isolated from your Pydantic validation definitions (`schemas/`).
- **Use a `core` directory:** Keep configuration, security setups, and heavy startup scripts in a dedicated `core` folder rather than polluting `main.py`.
- **The Application Factory:** In `main.py`, create a function like `create_app() -> FastAPI:` that builds the app instance. This makes writing tests vastly easier later.

## Common Mistakes
- **Putting business logic in the APIRouter:** Your router file should only receive the request, validate it, and immediately pass it to a `service`. Do not write 50 lines of complex math or database queries directly inside an `@app.get` endpoint!
- **Circular Imports:** If `models` import `schemas` and `schemas` import `models`, Python will crash. Strict structuring prevents this.

## Interview Questions
**Q: FastAPI does not enforce a directory structure. How do you decide how to structure a large app?**
A: I use domain-driven or layer-driven design. I separate the web layer (routers), business logic layer (services), validation layer (schemas/Pydantic), and data layer (models/SQLAlchemy) to ensure exact Separation of Concerns.

**Q: Where should you store sensitive data like API keys and database passwords?**
A: Sensitive data should be loaded from a `.env` file via environment variables. These variables should be validated at startup using Pydantic's `BaseSettings` within the `core/config.py` module.
