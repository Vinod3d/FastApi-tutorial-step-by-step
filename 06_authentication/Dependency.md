यह file **FastAPI Dependency Injection system** के लिए बनाई गई है।
इसका काम है **बार-बार लिखे जाने वाले common logic (token verify, DB session, services)** को reusable बनाना।

यानी API route में आपको हर बार:

* token decode
* DB session create
* seller fetch
* service create

नहीं लिखना पड़ेगा।

FastAPI खुद ये dependencies inject कर देगा।

यह feature FastAPI का बहुत powerful part है।

---

# Dependency File Explained

| No. | Topic                                                                 |
| --- | --------------------------------------------------------------------- |
| 1   | [Why Dependency File Exists](#1-why-dependency-file-exists)           |
| 2   | [Database Session Dependency](#2-database-session-dependency)         |
| 3   | [Access Token Dependency](#3-access-token-dependency)                 |
| 4   | [Get Current Seller](#4-get-current-seller)                           |
| 5   | [Service Dependencies](#5-service-dependencies)                       |
| 6   | [Annotated Shortcut Dependencies](#6-annotated-shortcut-dependencies) |
| 7   | [How It Is Used In Routes](#7-how-it-is-used-in-routes)               |

---

# 1 Why Dependency File Exists

Imagine every route needs:

```
token verify
DB session
seller fetch
shipment service
```

Without dependency system:

```python
@app.get("/orders")
async def get_orders(token: str, session: AsyncSession):
```

You would repeat **lots of code**.

So dependencies help to **centralize logic**.

---

# 2 Database Session Dependency

```python
SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

Meaning:

```
SessionDep = database session dependency
```

`get_session` function creates DB session.

Example usage later:

```python
session: SessionDep
```

FastAPI automatically provides database session.

Async session comes from SQLAlchemy.

---

# 3 Access Token Dependency

```python
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme_seller)]):
```

Step 1
FastAPI extracts token from header.

Header example:

```
Authorization: Bearer TOKEN
```

The token is extracted using:

```
oauth2_scheme_seller
```

---

### Decode Token

```python
data = decode_access_token(token)
```

This function decodes JWT token.

JWT library commonly used is python-jose.

---

### Check blacklist

```python
await is_jti_blacklisted(data["jti"])
```

This checks if token is revoked.

Stored inside:

```
Redis
```

Using Redis.

Example:

```
logout token → add to blacklist
```

---

### Invalid token

```python
raise HTTPException(status_code=401)
```

If token invalid → user blocked.

---

# 4 Get Current Seller

```python
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_access_token)],
    session: SessionDep
) -> Seller:
```

This dependency:

1️⃣ gets decoded token
2️⃣ gets DB session
3️⃣ fetches seller from database

---

### Fetch seller

```python
seller = await session.get(Seller, UUID(token_data["user"]["id"]))
```

Meaning:

```
SELECT * FROM seller WHERE id = ?
```

If seller not found:

```python
raise HTTPException(status_code=404)
```

---

### Return seller object

```python
return seller
```

Now API route receives **seller object automatically**.

---

# 5 Service Dependencies

These create **service layer objects**.

Example:

```python
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)
```

Meaning:

```
ShipmentService(session)
```

Service handles business logic.

---

Same for seller:

```python
def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)
```

This is **clean architecture pattern**.

```
Route → Service → Database
```

---

# 6 Annotated Shortcut Dependencies

Example:

```python
SellerDep = Annotated[
    Seller,
    Depends(get_current_seller),
]
```

Meaning:

```
SellerDep = logged in seller
```

Instead of writing:

```python
seller: Seller = Depends(get_current_seller)
```

You can write:

```python
seller: SellerDep
```

Much cleaner.

---

Same for services.

Shipment service:

```python
ShipmentServiceDep = Annotated[
    ShipmentService,
    Depends(get_shipment_service),
]
```

Seller service:

```python
SellerServiceDep = Annotated[
    SellerService,
    Depends(get_seller_service),
]
```

---

# 7 How It Is Used In Routes

Example route:

```python
@app.get("/shipments")
async def get_shipments(
    seller: SellerDep,
    shipment_service: ShipmentServiceDep
):
    return await shipment_service.get_shipments(seller.id)
```

FastAPI automatically does:

```
1 extract token
2 decode JWT
3 check blacklist
4 fetch seller
5 create shipment service
```

All automatically.

---

# Real Execution Flow

```
Request
   ↓
Authorization Header
   ↓
oauth2_scheme extracts token
   ↓
get_access_token()
   ↓
decode JWT
   ↓
check Redis blacklist
   ↓
get_current_seller()
   ↓
fetch seller from DB
   ↓
inject seller into route
```

---

# Simple Explanation

This dependency file provides:

```
database session
JWT authentication
seller retrieval
service creation
```

So routes stay **clean and simple**.

Example final route:

```
@app.get("/orders")
async def get_orders(
    seller: SellerDep,
    shipment_service: ShipmentServiceDep
)
```

No authentication code needed inside route.

---

✅ This is **professional backend architecture** used in many FastAPI projects.

---

If you want, I can also show you **a visual diagram of this dependency flow (Route → Dependency → Service → Database)** which makes this concept extremely easy to understand.
