from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import json
import time
import asyncio
import uvicorn

app = FastAPI(title="SSE vs WebSocket Comparison")
app.mount("/public", StaticFiles(directory="public"), name="public")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

# Global state
sse_clients = 0
messages_sent = 0
start_time = time.time()
ws_manager = ConnectionManager()

@app.get("/sse")
async def sse_stream():
    global sse_clients, messages_sent
    sse_clients += 1
    client_id = sse_clients
    print(f"🚀 SSE client #{client_id} connected. Total: {sse_clients}")
    
    async def generate():
        global messages_sent
        counter = 0
        try:
            while True:
                data = {
                    'ts': int(time.time() * 1000),
                    'seq': counter,
                    'protocol': 'FastAPI-SSE',
                    'client_id': client_id
                }
                yield f"data: {json.dumps(data)}\n\n"
                counter += 1
                messages_sent += 1
                await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ SSE client #{client_id} error: {e}")
        finally:
            global sse_clients
            sse_clients -= 1
            print(f"🔌 SSE client #{client_id} disconnected. Total: {sse_clients}")
    
    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global messages_sent
    await ws_manager.connect(websocket)
    client_id = len(ws_manager.active_connections)
    print(f"🚀 WebSocket client #{client_id} connected. Total: {len(ws_manager.active_connections)}")
    
    try:
        counter = 0
        while True:
            data = {
                'ts': int(time.time() * 1000),
                'seq': counter,
                'protocol': 'FastAPI-WS',
                'client_id': client_id
            }
            await websocket.send_text(json.dumps(data))
            counter += 1
            messages_sent += 1
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        print(f"🔌 WebSocket client #{client_id} disconnected. Total: {len(ws_manager.active_connections)}")

@app.get("/api/stats")
async def get_stats():
    return {
        'sseClients': sse_clients,
        'wsClients': len(ws_manager.active_connections),
        'messagesSent': messages_sent,
        'uptime': int((time.time() - start_time) * 1000),
        'server': 'FastAPI',
        'timestamp': int(time.time() * 1000)
    }

@app.get("/api/reset")
async def reset_stats():
    global messages_sent, start_time
    messages_sent = 0
    start_time = time.time()
    return {"status": "Statistics reset"}

@app.get("/")
async def serve_dashboard():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI - SSE vs WebSocket</title>
        <meta http-equiv="refresh" content="0;url=/public/index.html">
    </head>
    <body>
        <p>Redirecting to <a href="/public/index.html">dashboard</a>...</p>
    </body>
    </html>
    """)

if __name__ == "__main__":
    print("🎯 FastAPI Server starting...")
    print("📍 SSE Endpoint: http://localhost:8000/sse")
    print("📍 WebSocket Endpoint: ws://localhost:8000/ws") 
    print("📍 Dashboard: http://localhost:8000/public/index.html")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")