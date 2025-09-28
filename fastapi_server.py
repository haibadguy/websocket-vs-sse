from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import json
import time
import asyncio

app = FastAPI()

# Client tracking
sse_clients = 0
messages_sent = 0
start_time = time.time()

@app.get("/sse")
async def sse_stream():
    global sse_clients, messages_sent
    sse_clients += 1
    print(f"SSE client connected. Total: {sse_clients}")
    
    async def generate():
        global messages_sent, sse_clients
        counter = 0
        try:
            while True:
                data = {
                    'ts': int(time.time() * 1000),
                    'seq': counter,
                    'protocol': 'FastAPI-SSE'
                }
                yield f"data: {json.dumps(data)}\n\n"
                counter += 1
                messages_sent += 1
                await asyncio.sleep(1)
        except Exception:
            sse_clients -= 1
            print(f"SSE client disconnected. Total: {sse_clients}")
    
    return StreamingResponse(
        generate(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.get("/api/stats")
async def stats():
    return {
        'sseClients': sse_clients,
        'wsClients': 0,  # WebSocket requires additional setup
        'messagesSent': messages_sent,
        'uptime': int((time.time() - start_time) * 1000)
    }

@app.get("/", response_class=HTMLResponse)
async def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>FastAPI SSE Demo</title></head>
    <body>
        <h1>FastAPI SSE Demo</h1>
        <div>Messages: <span id="count">0</span></div>
        <div>Latency: <span id="latency">0ms</span></div>
        <script>
            let count = 0;
            const es = new EventSource('/sse');
            es.onmessage = event => {
                const data = JSON.parse(event.data);
                const latency = Date.now() - data.ts;
                document.getElementById('count').textContent = ++count;
                document.getElementById('latency').textContent = latency + 'ms';
            };
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    import uvicorn
    print("FastAPI SSE server running on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)