# Monolith vs Microservices

## What you will learn
- The definition and benefits of a Monolithic Architecture
- When and why companies split into Microservices
- The Hidden Costs of Microservices
- How FastAPI fits perfectly into both patterns

## Concept (Simple Explanation)
**Monolith:** A Swiss Army Knife. It has a knife, a screwdriver, a corkscrew, and a pair of scissors all built into one single physical object. It is easy to carry and simple to use. If the knife breaks, you have to throw the whole tool away and buy a new one.

**Microservices:** A Toolbox. You have a distinct, separate knife, a separate screwdriver, and separate scissors. If the knife breaks, you throw it away and buy just a new knife. But carrying the entire toolbox requires much more effort than a Swiss Army Knife.

## The Monolithic Architecture
In a Monolith, your User Authentication, your Product Catalog, and your Payment Processing all exist in the exact same FastAPI application (`main.py`), sharing the exact same PostgreSQL database.

**Pros:**
- Incredibly easy to develop, test, and deploy (just run `git push` and one Docker container).
- Zero network latency between components. Finding a User's Products is just a split-second SQL `JOIN`.

**Cons:**
- If the Payment Processing code has a memory leak and crashes the server, the entire application (including User Login) goes down instantly.
- Codebase becomes impossibly large for 100+ developers to work on simultaneously without merge conflicts.

## The Microservices Architecture
In Microservices, you have 3 totally separate FastAPI applications running on 3 different servers, with 3 totally separate databases. 
- *Auth Service* (Handles log in)
- *Product Service* (Handles inventory)
- *Payment Service* (Handles credit cards)

**Pros:**
- **Independent Scaling:** If it's Black Friday, the *Payment Service* is getting crushed with traffic. We can spin up 50 copies of the Payment Service, while leaving the Auth Service at 2 copies, saving massive AWS costs.
- **Resilience:** If the *Product Service* crashes, users can still log in and update their billing info on the *Auth Service*.

**Cons:**
- **Data consistency:** You cannot do a SQL `JOIN` across two separate databases.
- **Latency:** Services must talk to each other over HTTP or message queues, which takes 50ms instead of 0.5ms.
- **Complexity:** You need Kubernetes, Docker orchestration, and advanced DevOps just to deploy the app.

## Interview Questions
**Q: "I am building a brand new startup from scratch. Should I start with Microservices to ensure we scale?"**
A: Absolutely not! You should always start with a modular monolith. Microservices solve organizational and massive traffic scaling problems that startups do not have. Starting with microservices will stall your development velocity due to DevOps overhead. Build a monolith, separate your folders cleanly by domain (users vs products), and extract them into microservices 3 years later ONLY if the monolith breaks under user load.
