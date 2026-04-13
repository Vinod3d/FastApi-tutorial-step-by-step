# Delivery Partner Model Implementation (Step-by-Step)


# 1 Create Base User Model

Both **Seller and DeliveryPartner are users**, so we create a **base model** containing common user fields.

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel):
    email: str
    password: str
    name: str
```

Important:

* `table=True` is **not used** here.
* This model will **only be used for inheritance**.

---

# 2 Create Seller Model Using User Inheritance

Seller inherits from **User + SQLModel**.

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Seller(User, SQLModel, table=True):
    __tablename__ = "seller"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
```

Explanation:

* `User` fields automatically come here.
* `id` is the primary key.

---

# 3 Create DeliveryPartner Model

Create a model similar to Seller.

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class DeliveryPartner(User, SQLModel, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
```

Important note:

Each table **must define its own primary key**.

---

# 4 Add Delivery Partner Specific Fields

Delivery partner needs:

1. **Serviceable zip codes**
2. **Maximum shipment capacity**

Because zip codes are stored as **list**, we must use **SQLAlchemy column**.

```python
from typing import List
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import ARRAY

class DeliveryPartner(User, SQLModel, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    serviceable_zip_codes: List[int] = Field(
        sa_column=Column(ARRAY(Integer))
    )

    max_handling_capacity: int
```

Explanation:

* `ARRAY(Integer)` stores **list of integers** in PostgreSQL.

Example:

```
[462001, 462002, 462003]
```

---

# 5 Create Shipment Model Foreign Key

Shipment must store **which delivery partner is assigned**.

```python
from uuid import UUID
from sqlmodel import Field

class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    delivery_partner_id: UUID | None = Field(
        default=None,
        foreign_key="delivery_partner.id"
    )
```

Explanation:

* This creates a **foreign key relationship**.

---

# 6 Create Relationships Between Models

Relationships help us access related data easily.

### Shipment Side

```python
from sqlmodel import Relationship

class Shipment(SQLModel, table=True):

    delivery_partner_id: UUID | None = Field(
        default=None,
        foreign_key="delivery_partner.id"
    )

    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments"
    )
```

---

### Delivery Partner Side

```python
from typing import List

class DeliveryPartner(User, SQLModel, table=True):

    shipments: List["Shipment"] = Relationship(
        back_populates="delivery_partner"
    )
```

Now:

```
delivery_partner -> shipments
shipment -> delivery_partner
```

Both sides are connected.

---

# 7 Add created_at Timestamp Field

We track when records are created.

```python
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP

created_at: datetime = Field(
    sa_column=Column(
        TIMESTAMP,
        default=datetime.utcnow
    )
)
```

Add this field to:

* Seller
* DeliveryPartner
* Shipment

Example:

```python
created_at: datetime = Field(
    sa_column=Column(TIMESTAMP, default=datetime.utcnow)
)
```

---

# 8 Set Custom Table Names

To avoid guessing table names.

Example:

```python
__tablename__ = "delivery_partner"
```

Also set for:

```
seller
shipment
```

---

# 9 Install and Initialize Alembic

Install Alembic:

```bash
pip install alembic
```

Initialize migrations:

```bash
alembic init -t async migrations
```

This creates:

```
migrations/
alembic.ini
env.py
versions/
```

---

# 10 Configure Alembic Environment

Open:

```
migrations/env.py
```

### Set database URL

```python
config.set_main_option(
    "sqlalchemy.url",
    settings.POSTGRES_URL
)
```

---

### Set target metadata

```python
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata
```

---

### Import models

Alembic must know models.

```python
from app.database.models import Shipment
from app.database.models import Seller
from app.database.models import DeliveryPartner
```

---

# 11 Generate Migration Script

Create migration revision.

```bash
alembic revision --autogenerate -m "adding delivery partner"
```

This creates a file in:

```
migrations/versions/
```

Example:

```
2024_add_delivery_partner.py
```

---

# 12 Fix SQLModel Import Issue

Sometimes migration file needs SQLModel import.

Add this at top:

```python
import sqlmodel
```

To avoid repeating in future:

Edit:

```
script.py.mako
```

Add:

```python
import sqlmodel
```

---

# 13 Run Migration

Apply database changes.

```bash
alembic upgrade head
```

This executes the migration script.

---

# 14 Verify Tables in Database

Open **pgAdmin**.

Refresh tables.

You should see:

```
seller
delivery_partner
shipment
```

Now the **delivery_partner table is successfully added**.

---

# Final Result

Your system now supports:

* Seller users
* Delivery partner users
* Shipment assignment
* Zip code service tracking
* Shipment capacity control
* Automatic timestamps
* Database migrations using Alembic
