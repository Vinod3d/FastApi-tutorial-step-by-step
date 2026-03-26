# WebSockets in FastAPI

## What you will learn
- The difference between HTTP polling and WebSockets
- Establishing persistent two-way connections
- Receiving and Sending data in real-time
- Building a basic chat room (Connection Manager)

## Concept (Simple Explanation)
**Standard HTTP:** You send a letter in the mail asking "Do I have any new messages?" The server replies "No." You ask again. The server replies "No." You ask again. (Very slow and inefficient).

**WebSockets:** You pick up a telephone, call the server, and **keep the line open**. Now, the moment the server gets a message, it instantly speaks it through the phone. You can both talk and listen continuously without hanging up.

WebSockets are mandatory for Chat Applications, Live Sports Scores, Crypto Trading Tickers, and multiplayer games.

## Code Example
**1. A Simple Echo Server**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/echo")
async def websocket_echo_endpoint(websocket: WebSocket):
    # 1. Accept the incoming telephone call from the client
    await websocket.accept()
    
    try:
        # 2. Keep the line open indefinitely using a while loop!
        while True:
            # 3. Wait for the client to say something
            data = await websocket.receive_text()
            
            # 4. Talk back to the client
            await websocket.send_text(f"Server says: You wrote {data}")
            
    except WebSocketDisconnect:
        # Handle the client hanging up the phone
        print("Client disconnected!")
```

**2. Broadcasting to Multiple Clients (Chat Room)**
To make a chat room, you need to remember *everyone's* open `WebSocket` connection in a List. When one person speaks, you iterate through the list and send the text to everyone.

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
# Use this manager inside your websocket endpoint!
```

## Best Practices
- **Use Heartbeats/Pings:** Browsers and Load Balancers automatically kill WebSockets if no data is sent for ~60 seconds. You must implement a "Ping-Pong" mechanism where the server sends a tiny empty message every 30 seconds to keep the line alive.
- **Implement rate limiting:** WebSockets can receive hundreds of messages per second. A malicious user can spam a websocket and crash your server instantly since the connection bypasses standard HTTP firewalls.

## Common Mistakes
- **Using WebSockets for everything:** WebSockets do not have built-in headers, status codes (404, 500), or native JSON routing. If you just want to fetch a user profile, stick to standard HTTP GET requests!
- **Not handling `WebSocketDisconnect`:** If the user closes their browser tab, the `receive_text()` function will crash with a specific exception. If you don't `try/except` it, it will crash the background task handling that socket.

## Interview Questions
**Q: Why doesn't regular HTTP REST work well for a real-time chat application?**
A: Because HTTP is strictly stateless and "Client-Driven." The server cannot talk unless spoken to. To get real-time chat via HTTP, the client would have to "Long-Poll" (ask the server every 500ms if a new message exists), completely flooding the network and wasting massive bandwidth with HTTP headers.

**Q: Does FastAPI natively support WebSockets?**
A: Yes, beautifully. Because FastAPI is built on Starlette and runs on ASGI (Asynchronous Server Gateway Interface), it was designed from the ground up to natively handle long-lived asynchronous socket connections seamlessly alongside standard HTTP endpoints.
