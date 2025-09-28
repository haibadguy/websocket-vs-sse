from flask import Flask, Response, jsonify
import json
import time
import threading

app = Flask(__name__)

# Client tracking
sse_clients = 0
messages_sent = 0
start_time = time.time()

@app.route('/sse')
def sse_stream():
    global sse_clients, messages_sent
    sse_clients += 1
    print(f"SSE client connected. Total: {sse_clients}")
    
    def generate():
        global messages_sent
        counter = 0
        try:
            while True:
                data = {
                    'ts': int(time.time() * 1000),
                    'seq': counter,
                    'protocol': 'Flask-SSE'
                }
                yield f"data: {json.dumps(data)}\n\n"
                counter += 1
                messages_sent += 1
                time.sleep(1)
        except GeneratorExit:
            global sse_clients
            sse_clients -= 1
            print(f"SSE client disconnected. Total: {sse_clients}")
    
    return Response(generate(), 
                   content_type='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'Access-Control-Allow-Origin': '*'
                   })

@app.route('/api/stats')
def stats():
    return jsonify({
        'sseClients': sse_clients,
        'wsClients': 0,  # Flask doesn't handle WebSocket natively
        'messagesSent': messages_sent,
        'uptime': int((time.time() - start_time) * 1000)
    })

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Flask SSE Demo</title></head>
    <body>
        <h1>Flask SSE Demo</h1>
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

if __name__ == '__main__':
    print("Flask SSE server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)