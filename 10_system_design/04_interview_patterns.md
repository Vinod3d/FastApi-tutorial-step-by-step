# System Design Interview Patterns

## What you will learn
- How to answer System Design questions like a Senior Engineer
- Handling data scale (Sharding, Replication)
- Drawing out the architecture on a whiteboard
- The CAP Theorem

## Concept (Simple Explanation)
In Senior Backend Interviews, you won't just be asked "How to write a FastAPI route."
You will be asked: *"Design Twitter."* or *"Design an API that handles 100 Million requests an hour."*

You cannot memorize the answers to these. You must master the **Patterns of Scale**.

### 1. Database Replication (Leader-Follower)
A single database can handle maybe 10,000 queries a second. What if you get 50,000 read requests a second?
**Solution:** You create one "Leader" database, and 5 "Follower" databases. 
- Every time FastAPI executes an `INSERT/UPDATE/DELETE`, it goes to the **Leader**.
- The Leader instantly copies that new data to the 5 Followers.
- Every time FastAPI executes a `SELECT` (Read), it asks one of the 5 **Followers**. Since Twitter is 99% reading and 1% writing, this elegantly balances the massive read traffic!

### 2. Database Sharding
What happens when your database hits 5 Terabytes of data and refuses to run fast anymore because the table goes on forever?
**Solution:** You "Shard" the database. You literally split it into pieces based on a Shard Key (e.g., Region). 
- Users in USA are saved exclusively in Database A.
- Users in Europe are saved exclusively in Database B.
Suddenly, your queries run twice as fast because they only have to search half the data.

### 3. The CAP Theorem
The golden rule of distributed systems. It states a system can only guarantee 2 out of these 3 things during a network failure:
1. **Consistency (C):** Every single user sees the exact same data at the exact same moment. (Crucial for Bank Balances).
2. **Availability (A):** The system always returns an answer, even if the answer is slightly outdated. (Crucial for Instagram Likes).
3. **Partition Tolerance (P):** The system successfully operates even if a networking cable is cut between 2 servers.

*(Hint: In the modern cloud, networks ALWAYS fail. You cannot sacrifice P. Therefore, you must choose between C and A!)*

## Approaching the Interview Question
If asked "Design an E-Commerce site", never instantly start writing database schemas.

**Follow the 4 steps:**
1. **Clarify Requirements (5 mins):** "Are we designing the frontend too, or just the backend APIs? How many users do we expect per day? Do we need to handle payment processing ourselves?"
2. **Back of the Envelope Math (5 mins):** "If we have 10M users generating 50kb of data a day, we need 500GB of storage a day, or 180TB a year. A single Postgres DB cannot hold this."
3. **High-Level Design (15 mins):** Draw the boxes. `[Client] -> [Load Balancer] -> [API Gateway / FastAPI] -> [Redis Cache] -> [Database]`.
4. **Deep Dive (15 mins):** Zoom in on the bottleneck. "The biggest issue here is Black Friday flash sales crashing the inventory DB. We will implement Apache Kafka message queues to buffer the checkout requests so the DB doesn't die."

## Conclusion
If you can fluently explain everything in this `10_system_design` chapter—from Load Balancing FastAPI to implementing Kafka over direct HTTP, you will pass virtually any modern backend system design interview.
