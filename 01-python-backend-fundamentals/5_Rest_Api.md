
# Chapter 1.5 REST API Concepts


## 1. What is an API?

API = Application Programming Interface

It allows two systems to communicate with each other.

Example:

* Mobile app talks to backend server
* Frontend talks to backend
* Backend talks to payment gateway

### Simple Definition:

An API is a bridge that allows different software systems to communicate.


## 2. What is a REST API?

REST = Representational State Transfer

It is an architectural style for building web APIs.

### Interview Definition:

REST is an architectural style that defines a set of constraints for designing scalable and stateless web services using HTTP methods.


## 3. REST Principles

A system is RESTful if it follows these rules:


### 1️⃣ Client-Server Architecture

* Client and server are separate
* Frontend doesn’t know how backend works
* Backend doesn’t care how frontend looks


### 2️⃣ Stateless

Every request must contain all necessary information.

Server does NOT store client session data.

Example:
User login → token sent in every request.


### 3️⃣ Cacheable

Responses should define whether they can be cached.

Improves performance.


### 4️⃣ Uniform Interface

Standard structure for all APIs.

Example:

```
GET /users
POST /users
GET /users/1
PUT /users/1
DELETE /users/1
```

### 5️⃣ Layered System

Client cannot tell if it is connected directly to server or through proxy/load balancer.


## 4. HTTP Methods in REST

Very important for interviews.

- **GET :** Used to retrieve data.
- **POST:** Used to create new resource.
- **PUT:** Used to update entire resource.
- **PATCH:** Used to update partial resource.
- **DELETE**  Used to delete resource.

### Interview Question:

Difference between PUT and PATCH?

PUT → Replaces full resource
PATCH → Updates only specific fields


## 5. What is a Resource?

Resource = Any object or data.

Example:

* User
* Product
* Order

In REST, everything is treated as a resource.

## 6. What is URI?

URI = Uniform Resource Identifier

Example:

```
https://api.example.com/users/1
```

Structure:

* Base URL
* Resource
* Resource ID


## 7. Status Codes

Backend interview always asks this.


## 2xx → Success

* 200 → OK
* 201 → Created
* 204 → No Content


## 4xx → Client Error

* 400 → Bad Request
* 401 → Unauthorized
* 403 → Forbidden
* 404 → Not Found


## 5xx → Server Error

* 500 → Internal Server Error
* 502 → Bad Gateway
* 503 → Service Unavailable

You must remember these.


# 🎯 Interview Rapid Fire

1. What is REST?
2. What is difference between PUT and PATCH?
3. What is stateless?
4. What is idempotent?
5. What are HTTP status codes?
6. What is resource in REST?
7. Why REST is preferred over SOAP?

You must answer confidently.