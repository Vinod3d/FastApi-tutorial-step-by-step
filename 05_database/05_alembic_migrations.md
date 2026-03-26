# Alembic Database Migrations

## What you will learn
- Why `create_all()` is unacceptable in production
- Managing database versions over time (Migrations)
- Configuring and generating Alembic migrations automatically
- Upgrading and Downgrading databases

## Concept (Simple Explanation)
Imagine you write a book, and it's printed (Database v1). A month later, you realize you need to add a new chapter. You can't just burn all existings books and rewrite it from scratch (data loss). You need to issue an "Addendum" pamphlet that tells people "Insert this new page after page 42."

**Alembic** writes those pamphlets. When you add a new column to your SQLAlchemy model (like `age`), Alembic looks at the code, looks at the live database, and generates a safe SQL script (`ALTER TABLE users ADD COLUMN age INT`) to safely update the database without deleting the user's data.

## Code Example
**1. Initialize Alembic (Terminal)**
```bash
pip install alembic
alembic init alembic
```

**2. Link Alembic to your database (`alembic.ini`)**
```ini
# Find this line and update it to your DB string
sqlalchemy.url = mysql+pymysql://root:password@localhost:3306/fastapi_db
```

**3. Link Alembic to your Models (`alembic/env.py`)**
```python
import sys, os
sys.path.append(os.getcwd())

# Import your Base model so Alembic can read your tables natively
from app.models import Base
target_metadata = Base.metadata
```

**4. Generate a Migration (After changing `models.py`)**
```bash
# This scans your models and generates the exact SQL diff!
alembic revision --autogenerate -m "added age column to user table"
```

**5. Apply the Migration**
```bash
# This actually executes the SQL against the live database
alembic upgrade head
```

## Best Practices
- **Commit your migrations to Git:** The `alembic/versions/` folder contains Python files representing every state change your database has ever made. These MUST be pushed to your repository so your teammates and production servers can run them.
- **Remove `metadata.create_all()`:** Once you adopt Alembic, remove `models.Base.metadata.create_all(bind=engine)` from your `main.py`. Let Alembic handle 100% of the table creation.

## Common Mistakes
- **Manually editing the database:** If you log into pgAdmin or MySQL Workbench and add a column manually, Alembic loses track of the "truth" and your next autogenerate will crash or break. Always let Alembic make the changes!
- **Not defining a target metadata:** If `target_metadata = None` in `env.py`, the `--autogenerate` flag will silently do nothing because Alembic doesn't know where your models live.

## Interview Questions
**Q: What is a Database Migration, and why use Alembic?**
A: A migration is a version-controlled script that systematically applies (or reverts) changes to a database schema. Alembic is the native migration tool for SQLAlchemy. It is critical for production because dropping and recreating tables to add a column would result in catastrophic data loss.

**Q: What does the command `alembic downgrade -1` do?**
A: It executes the "downgrade" function inside the most recently applied migration file, effectively reverting/undoing the last change you made to the database schema (like safely dropping a newly introduced column).
