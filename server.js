const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
app.use(express.static('public'));

// Client tracking
let sseClients = 0;
let wsClients = 0;
let messagesSent = 0;
const startTime = Date.now();

// SSE endpoint
app.get('/sse', (req, res) => {
  sseClients++;
  console.log(`SSE client connected. Total: ${sseClients}`);
  
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  let counter = 0;
  const interval = setInterval(() => {
    const payload = {
      ts: Date.now(),
      seq: counter++,
      protocol: 'SSE'
    };
    res.write(`data: ${JSON.stringify(payload)}\n\n`);
    messagesSent++;
  }, 1000);

  req.on('close', () => {
    clearInterval(interval);
    sseClients--;
    console.log(`SSE client disconnected. Total: ${sseClients}`);
  });
});

// Stats API endpoint
app.get('/api/stats', (req, res) => {
  res.json({
    sseClients,
    wsClients,
    messagesSent,
    uptime: Date.now() - startTime
  });
});

// WebSocket server
const server = http.createServer(app);
const wss = new WebSocket.Server({ server, path: '/ws' });

let wsCounter = 0;
const wsInterval = setInterval(() => {
  const payload = {
    ts: Date.now(),
    seq: wsCounter++,
    protocol: 'WebSocket'
  };
  const msg = JSON.stringify(payload);
  
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(msg);
      messagesSent++;
    }
  });
}, 1000);

wss.on('connection', ws => {
  wsClients++;
  console.log(`WebSocket client connected. Total: ${wsClients}`);
  
  ws.on('close', () => {
    wsClients--;
    console.log(`WebSocket client disconnected. Total: ${wsClients}`);
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
