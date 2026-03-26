

# Custom Responses in FastAPI

By default, FastAPI returns:

* JSON
* Status code 200

But sometimes you need:

* Custom JSON response
* HTML page
* File download
* Redirect
* Streaming large data
* Custom headers
* Cookies

That’s where **custom responses** come in.

## 1️⃣ JSONResponse

Used when you want:

* Custom status code
* Custom headers
* Manual response control

```python
from fastapi.responses import JSONResponse

@app.get("/custom")
def custom_response():
    return JSONResponse(
        status_code=201,
        content={"message": "Created successfully"}
    )
```
### 🔥 Interview Use Case

When you need:

* Dynamic status codes
* Custom response structure
* Additional headers

## 2️⃣ HTMLResponse

Used when returning HTML content.

```python
from fastapi.responses import HTMLResponse

@app.get("/html", response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """
```

### When is this used?

* Serving simple frontend pages
* Admin panels
* Static content

## 3️⃣ FileResponse

Used to return files.

```python
from fastapi.responses import FileResponse

@app.get("/download")
def download_file():
    return FileResponse("sample.pdf")
```

### Real-world Use Case

* PDF invoice download
* Image serving
* CSV export
* Report generation

## 4️⃣ RedirectResponse

Used to redirect user to another URL.

```python
from fastapi.responses import RedirectResponse

@app.get("/google")
def redirect_to_google():
    return RedirectResponse("https://www.google.com")
```

### Interview Question

❓ What status code is used for redirect?

* 302 (Temporary redirect)
* 307 (Preserve method)
* 308 (Permanent redirect)

## 5️⃣ StreamingResponse

Used for:

* Large files
* Video streaming
* Real-time data

```python
from fastapi.responses import StreamingResponse

def fake_stream():
    for i in range(5):
        yield f"Chunk {i}\n"

@app.get("/stream")
def stream():
    return StreamingResponse(fake_stream(), media_type="text/plain")
```

### Why use Streaming?

* Memory efficient
* Doesn't load entire file into memory
* Better for large data

## 6️⃣ Custom Headers

```python
from fastapi import Response

@app.get("/headers")
def custom_headers(response: Response):
    response.headers["X-App-Name"] = "FastAPI Tutorial"
    return {"message": "Header added"}
```

## 7️⃣ Setting Cookies

```python
@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="username", value="Vinod")
    return {"message": "Cookie set"}
```

## 8️⃣ Custom Response Class

You can set default response type:

```python
@app.get("/example", response_class=HTMLResponse)
def example():
    return "<h1>Hello</h1>"
```

# 🔥 Advanced Interview Concept

### ❓ Difference between `response_model` and `response_class`?

| response_model           | response_class         |
| ------------------------ | ---------------------- |
| Controls data validation | Controls output format |
| Uses Pydantic            | Uses Response classes  |
| Filters fields           | Changes content type   |


# 🔥 When Should You Use Custom Response?

Use when:

* You need non-JSON output
* You want custom status code with full control
* You want file download
* You want streaming
* You want redirect



# 🚨 Common Mistakes

❌ Using JSONResponse unnecessarily
❌ Returning body with 204
❌ Not setting correct media_type in StreamingResponse
❌ Forgetting response_model when needed


