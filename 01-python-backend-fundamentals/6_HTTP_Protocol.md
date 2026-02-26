

# Chapter 1.6 HTTP Protocol


## 1. What is HTTP?

HTTP = HyperText Transfer Protocol

It is a communication protocol used between:

* Client (browser / mobile app)
* Server (backend)

It defines how messages are formatted and transmitted.

### 🔹 Interview Definition:

HTTP is a stateless application-layer protocol used for communication between clients and servers over the web.


## 2. Where HTTP Works (OSI Model)

HTTP works at:

👉 Application Layer (Layer 7)

It runs on top of:

* TCP (Transmission Control Protocol)
* Usually Port 80 (HTTP)
* Port 443 (HTTPS)

## 3. HTTP Request Structure

When client sends request, it looks like this:

```
GET /users HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer token
```

### Structure:

1. Request Line
2. Headers
3. Body (optional)


### 🔹 Request Line

```
GET /users HTTP/1.1
```

Contains:

* HTTP method
* URL
* HTTP version


### 🔹 Headers

Provide metadata about request.

Examples:

* Content-Type
* Authorization
* User-Agent
* Accept


### 🔹 Body

Used in:

* POST
* PUT
* PATCH

Example:

```json
{
  "name": "Vinod",
  "age": 25
}
```

## 4. HTTP Response Structure

Server sends:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Success"
}
```

### Structure:

1. Status Line
2. Headers
3. Body

## 5. HTTP Versions


- **HTTP/1.0:** One request per connection
- **HTTP/1.1:** Persistent connections Multiple requests on same connection
- **HTTP/2:** Faster, Multiplexing, Binary protocol
- **HTTP/3:** Uses QUIC (UDP based) Faster and secure

## 6. What is HTTPS?

HTTPS = HTTP + SSL/TLS encryption

It encrypts:

* Data
* Passwords
* Tokens

Port: 443

Without HTTPS → data can be intercepted.

## 7. Stateless Nature of HTTP

HTTP is stateless.

Server does NOT remember previous request.

That’s why:

* We use JWT tokens
* Sessions
* Cookies

## 8. Headers


### 🔹 Content-Type

Tells server what format body is in.

```
Content-Type: application/json
```

### 🔹 Authorization

Used for authentication.

```
Authorization: Bearer <token>
```

### 🔹 Accept

Tells server what response format client expects.

### 🔹 Cookie

Stores small data in browser.


## 9. Query Parameters vs Path Parameters

Example:

```
GET /users/1
```

1 → Path Parameter

Example:

```
GET /users?age=25
```

age=25 → Query Parameter

---

## 10. HTTP Status Code Categories


### 1xx → Informational

### 2xx → Success

### 3xx → Redirection

### 4xx → Client Error

### 5xx → Server Error


## 11. What is TCP Handshake?

Before HTTP communication:

1. SYN
2. SYN-ACK
3. ACK

Three-way handshake establishes connection.

Important networking interview topic.

## 12. Keep-Alive Connection

In HTTP/1.1:

Connection remains open
Improves performance


## 13. What is CORS?

Cross-Origin Resource Sharing

Browser security mechanism.

Example:
Frontend: localhost:3000
Backend: localhost:8000

Different origin → blocked unless CORS enabled.

FastAPI uses CORS middleware.


## 14. Difference Between HTTP and WebSocket

HTTP:

* Request-response
* Stateless

WebSocket:

* Persistent connection
* Real-time communication

FastAPI supports WebSockets.


## 15. Common Interview Questions

1. What is HTTP?
2. Difference between HTTP and HTTPS?
3. What is stateless?
4. What are headers?
5. What is CORS?
6. What is TCP handshake?
7. Difference between path and query parameters?
8. What is keep-alive?
9. What is HTTP version difference?


# 🧠 Backend Perspective (FastAPI Context)

When client sends request:

1. TCP connection established
2. HTTP request sent
3. FastAPI receives
4. ASGI server processes
5. Response returned

Understanding HTTP helps in:

* Debugging
* Writing correct APIs
* Handling errors
* Authentication