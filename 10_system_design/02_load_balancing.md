# Load Balancing & Scaling

## What you will learn
- Vertical vs Horizontal Scaling
- What a Load Balancer actually does
- Reverse Proxies (NGINX / AWS ALB)
- Sticky Sessions vs Stateless APIs

## Concept (Simple Explanation)
Imagine you own a highly successful Pizza Shop. You only have one Chef (Server). As more customers arrive, the Chef gets overwhelmed. 

**Vertical Scaling (Scaling Up):** You send the Chef to a ninja training camp and buy them energy drinks. They become 3x faster. (Upgrading your AWS EC2 server from 2GB RAM to 64GB RAM).
*Limit:* Eventually, humans can only move so fast. You hit a physical ceiling.

**Horizontal Scaling (Scaling Out):** You simply hire 5 new average-speed Chefs. (Starting 5 separate $5/month EC2 servers running your identical FastAPI app).
*Problem:* How do the customers know which Chef to hand their order to? 
*Solution:* The **Load Balancer**. You hire a Manager (NGINX/AWS ALB) to stand at the front door. The Manager takes the customer's order, looks at the 5 Chefs, sees which one is the least busy, and hands them the ticket.

## How it works in FastAPI
FastAPI apps should ideally be deployed behind a Load Balancer (like AWS Application Load Balancer, NGINX, or a Kubernetes Ingress).

1. The Internet sends an HTTP Request to `api.yourstartup.com`.
2. The DNS maps that to your Load Balancer's IP address.
3. The Load Balancer checks its list of 5 internal servers (running Gunicorn/Uvicorn).
4. Using an algorithm like `Round Robin` (taking turns 1, 2, 3, 4, 5, 1, 2...), the Load Balancer forwards the request to Server #3.
5. Server #3 computes the FastAPI response and sends it back to the Load Balancer.
6. The Load Balancer sends it back to the user. The user has no idea Server #3 did the work.

## Best Practices
- **Never store state on the server:** To use Horizontal Scaling, your API **must** be perfectly Stateless (which is why we use JWTs!). If Server #1 stores "User Logged In" in its RAM, and the Load Balancer sends their next request to Server #2, Server #2 will think they are logged out! With JWTs, every server can instantly verify the user.
- **Offload SSL/HTTPS:** Your FastAPI app should never handle SSL certificates or HTTPS directly. The Load Balancer should terminate the HTTPS connection (handling the heavy decryption math), and forward plain, fast HTTP to your internal FastAPI servers over a secure private network.

## Interview Questions
**Q: Explain the difference between Layer 4 and Layer 7 Load Balancing.**
A: A Layer 4 load balancer routes traffic based purely on network information (IP addresses and TCP ports). It is extremely fast but blind to the actual content. A Layer 7 load balancer (like an Application Load Balancer) can actually read the HTTP headers and URL paths. It can route `/users` traffic specifically to a User Microservice, and `/payments` traffic to a Payment Microservice.

**Q: What is "Round Robin"?**
A: It is the simplest and most common load balancing algorithm. The load balancer simply distributes newly incoming requests sequentially down the list of available servers in order (Server A, then B, then C, then back to A) ensuring an exactly even distribution of connection traffic.
