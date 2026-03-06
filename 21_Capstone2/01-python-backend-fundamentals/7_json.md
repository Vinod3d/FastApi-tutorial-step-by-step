

# Chapter 1.7 JSON & Serialization

## 1. What is JSON?

JSON = JavaScript Object Notation

It is a lightweight data format used to exchange data between:

* Client ↔ Server
* API ↔ API

### 🔹 Interview Definition:

JSON is a lightweight, text-based data interchange format that is easy for humans to read and write and easy for machines to parse and generate.

## 2. Why JSON is Used in APIs?

Because:

* Lightweight
* Easy to parse
* Language independent
* Human readable
* Fast

Modern APIs (including FastAPI) use JSON by default.

## 3. JSON Data Types

JSON supports:

| JSON Type | Example             |
| --------- | ------------------- |
| String    | `"Vinod"`           |
| Number    | `25`                |
| Boolean   | `true`              |
| Null      | `null`              |
| Array     | `[1,2,3]`           |
| Object    | `{"name": "Vinod"}` |


## 4. JSON vs Python Dictionary

Very important difference:

Python dict:

```python
{
    "name": "Vinod",
    "age": 25
}
```

JSON:

```json
{
    "name": "Vinod",
    "age": 25
}
```

Looks similar but:

* JSON keys must be double-quoted
* JSON true/false is lowercase
* JSON null instead of None

## 5. What is Serialization?

Serialization means:

👉 Converting Python object → JSON string

Example:

```python
import json

data = {"name": "Vinod", "age": 25}
json_data = json.dumps(data)
```

`dumps()` → convert to JSON string


## 6. What is Deserialization?

Deserialization means:

👉 Converting JSON string → Python object

Example:

```python
json_string = '{"name": "Vinod", "age": 25}'
data = json.loads(json_string)
```

`loads()` → convert to Python dict

## 7. Why Serialization is Important in FastAPI?

When client sends request:

JSON → Python object

When server responds:

Python object → JSON

FastAPI automatically handles this conversion.


## 8. Common Serialization Errors

### Error 1: Object not JSON serializable

Example:

```python
from datetime import datetime

data = {"time": datetime.now()}
```

This fails because datetime is not JSON serializable.

Solution:
Convert to string or use custom encoder.

## 9. What is Pydantic? (FastAPI Context)

FastAPI uses Pydantic models for:

* Data validation
* Serialization
* Deserialization

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

FastAPI automatically:

* Validates request data
* Converts to Python object
* Converts response back to JSON

## 10. JSON vs XML (Interview Question)

JSON:

* Lightweight
* Faster
* Modern
* Used in REST APIs

XML:

* Verbose
* Older
* Used in SOAP

Modern systems prefer JSON.


## 11. Content-Type Header 

When sending JSON:

```
Content-Type: application/json
```

If this header is wrong → server may not parse body correctly.


## 12. Nested JSON Example

```json
{
  "name": "Vinod",
  "skills": ["Python", "FastAPI"],
  "address": {
      "city": "Lucknow",
      "pin": 226001
  }
}
```

This is common in real-world APIs.


## 13. JSON Limitations

JSON does NOT support:

* Functions
* Comments
* Date type (directly)
* Tuple
* Set

Only basic types allowed.

## 14. Streaming JSON 

For large data:

* Instead of loading full JSON
* Data can be streamed

Used in large-scale systems.

## 15. Common Interview Questions

1. What is JSON?
2. Difference between JSON and dict?
3. What is serialization?
4. What is deserialization?
5. What is dumps vs loads?
6. Why JSON is preferred over XML?
7. What is Pydantic?
8. Why datetime causes serialization error?

You must answer clearly.

# 🧠 Backend Perspective (FastAPI)

When request comes:

1. HTTP body contains JSON
2. FastAPI parses JSON
3. Converts to Pydantic model
4. Validates data
5. Returns JSON response

Understanding JSON helps in:

* Debugging API errors
* Writing proper schemas
* Handling nested data
* Designing scalable APIs