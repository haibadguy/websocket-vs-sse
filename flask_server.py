from flask import Flask, Response, jsonify, send_from_directory
from flask_sock import Sock
import json
import time
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = Sock(app)

# Client tracking
sse_clients = 0
ws_clients = set()
messages_sent = 0
start_time = time.time()

def get_ws_client_count():
    return len(ws_clients)

@app.route('/sse')
def sse_stream():
    global sse_clients, messages_sent
    sse_clients += 1
    client_id = sse_clients
    print(f"🚀 SSE client #{client_id} connected. Total: {sse_clients}")
    
    def generate():
        global messages_sent
        counter = 0
        try:
            while True:
                data = {
                    'ts': int(time.time() * 1000),
                    'seq': counter,
                    'protocol': 'Flask-SSE',
                    'client_id': client_id
                }
                yield f"data: {json.dumps(data)}\n\n"
                counter += 1
                messages_sent += 1
                time.sleep(1)
        except GeneratorExit:
            global sse_clients
            sse_clients -= 1
            print(f"🔌 SSE client #{client_id} disconnected. Total: {sse_clients}")
    
    return Response(
        generate(), 
        content_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive', 
            'Access-Control-Allow-Origin': '*'
        }
    )

@sock.route('/ws')
def websocket_endpoint(ws):
    global messages_sent
    ws_clients.add(ws)
    client_id = len(ws_clients)
    print(f"🚀 WebSocket client #{client_id} connected. Total: {len(ws_clients)}")
    
    try:
        counter = 0
        while True:
            data = {
                'ts': int(time.time() * 1000),
                'seq': counter,
                'protocol': 'Flask-WS', 
                'client_id': client_id
            }
            ws.send(json.dumps(data))
            counter += 1
            messages_sent += 1
            time.sleep(1)
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        ws_clients.discard(ws)
        print(f"🔌 WebSocket client disconnected. Total: {len(ws_clients)}")

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'sseClients': sse_clients,
        'wsClients': len(ws_clients),
        'messagesSent': messages_sent,
        'uptime': int((time.time() - start_time) * 1000),
        'server': 'Flask',
        'timestamp': int(time.time() * 1000)
    })

@app.route('/api/reset', methods=['POST'])
def reset_stats():
    global messages_sent, start_time
    messages_sent = 0
    start_time = time.time()
    return jsonify({"status": "Statistics reset"})

@app.route('/')
def serve_dashboard():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    print("🎯 Flask Server starting...")
    print("📍 SSE Endpoint: http://localhost:5000/sse")
    print("📍 WebSocket Endpoint: ws://localhost:5000/ws")
    print("📍 Dashboard: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)