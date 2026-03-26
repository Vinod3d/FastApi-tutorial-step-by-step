# Authentication vs. Authorization

## What you will learn
- The fundamental difference between Authentication and Authorization
- Why confusing them causes critical security flaws
- How they practically apply to web applications
- Real-world flows mapping to FastAPI

## Concept (Simple Explanation)
**Authentication (AuthN):** *Who are you?*
When you approach a secure building, you hand the security guard your ID card. The guard verifies your face matches the photo. You are now Authenticated. (Logging in with email/password).

**Authorization (AuthZ):** *What are you allowed to do?*
Now that you are inside the building, you try to open the "Server Room" door, but your keycard glows red. You are authenticated (we know who you are), but you are not *authorized* (you do not have permission) to enter this specific room.

## Code Example
While we will code these concepts in the next files, understanding the HTTP flow is critical:

**1. Authentication Flow (Login)**
```text
Client -> POST /login (email="vinod@gmail.com", password="123")
Server -> Verifies in Database
Server -> Responds with 200 OK + JWT Token (Your ID Card)
```

**2. Authorization Flow (Accessing a Resource)**
```text
Client -> DELETE /users/5 (Header includes JWT Token)
Server -> Reads Token: "Identity = Vinod. Role = Standard User."
Server -> Checks Rule: "Can Standard Users delete accounts?"
Server -> Responds with 403 Forbidden (Your keycard failed)
```

## Best Practices
- **Handle Authentication First:** Always verify identity before checking permissions. If the user isn't logged in, instantly return a `401 Unauthorized`.
- **Default to Deny:** If an endpoint modifies data, explicitly require a role/permission. Never assume an endpoint is public by default unless it's a login or registration route.

## Common Mistakes
- **Mixing up 401 and 403 Status Codes:** 
  - `401 Unauthorized` actually means "Unauthenticated" (You are not logged in/Invalid Token). 
  - `403 Forbidden` means "Unauthorized" (You are logged in, but you don't have the right role). Returning a 401 when a standard user tries to access an admin panel is technically incorrect.

## Interview Questions
**Q: Explain the difference between Authentication and Authorization.**
A: Authentication (AuthN) proves a user's identity (e.g., verifying a password). Authorization (AuthZ) checks if that verified user has the correct permissions to perform a specific action or access a specific resource.

**Q: If a user successfully logs in but tries to delete an admin account they don't own, what HTTP status code should you return?**
A: `403 Forbidden`. The server understands who the user is (they are authenticated and not 401), but refuses to authorize the action.
