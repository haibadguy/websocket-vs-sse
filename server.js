const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
app.use(express.static('public'));

let sseClients = 0;
let wsClients = 0;
let messagesSent = 0;
const startTime = Date.now();

// Network simulation controls
let networkSimulation = {
  offline: false,
  latency: { min: 10, max: 50 },
  packetLoss: 0 // 0-100%
};

/**
 * SSE endpoint - ĐÃ SỬA
 */
app.get('/sse', (req, res) => {
  sseClients++;
  console.log(`✅ SSE connected. Total: ${sseClients}`);

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  // Send immediate connection confirmation
  res.write('data: {"type": "connected", "ts": ' + Date.now() + '}\n\n');

  let counter = 0;
  const interval = setInterval(() => {
    // Check if network is simulated offline
    if (networkSimulation.offline) {
      console.log('📵 SSE message dropped (offline simulation)');
      return;
    }
    
    // Simulate packet loss
    if (Math.random() * 100 < networkSimulation.packetLoss) {
      console.log('📦 SSE packet lost');
      return;
    }
    
    const payload = {
      ts: Date.now(),
      seq: counter++,
      protocol: 'SSE',
    };
    
    // Use simulated latency
    const { min, max } = networkSimulation.latency;
    const networkDelay = Math.random() * (max - min) + min;
    
    setTimeout(() => {
      try {
        res.write(`data: ${JSON.stringify(payload)}\n\n`);
        messagesSent++;
      } catch (err) {
        console.log('💥 SSE write error:', err.message);
      }
    }, networkDelay);
  }, 1000);

  req.on('close', () => {
    clearInterval(interval);
    sseClients = Math.max(0, sseClients - 1);
    console.log(`❌ SSE disconnected. Total: ${sseClients}`);
  });
  
  req.on('error', (err) => {
    clearInterval(interval);
    sseClients = Math.max(0, sseClients - 1);
    console.log(`💥 SSE error: ${err.message}. Total: ${sseClients}`);
  });
});

// Network simulation control endpoints
app.use(express.json());

app.post('/api/network/offline', (req, res) => {
  networkSimulation.offline = !networkSimulation.offline;
  console.log(`🌐 Network simulation: ${networkSimulation.offline ? 'OFFLINE' : 'ONLINE'}`);
  res.json({ offline: networkSimulation.offline });
});

app.post('/api/network/latency/:min/:max', (req, res) => {
  networkSimulation.latency.min = parseInt(req.params.min);
  networkSimulation.latency.max = parseInt(req.params.max);
  console.log(`⏱️ Latency simulation: ${networkSimulation.latency.min}-${networkSimulation.latency.max}ms`);
  res.json(networkSimulation.latency);
});

/**
 * Stats API
 */
app.get('/api/stats', (req, res) => {
  res.json({
    sseClients,
    wsClients,
    messagesSent,
    uptime: Date.now() - startTime,
    networkSimulation
  });
});

/**
 * WebSocket server - ĐÃ SỬA
 */
const server = http.createServer(app);
const wss = new WebSocket.Server({ server, path: '/ws' });

let wsCounter = 0;
setInterval(() => {
  // Check if network is simulated offline
  if (networkSimulation.offline) {
    console.log('📵 WebSocket message dropped (offline simulation)');
    return;
  }
  
  // Simulate packet loss
  if (Math.random() * 100 < networkSimulation.packetLoss) {
    console.log('📦 WebSocket packet lost');
    return;
  }
  
  const payload = {
    ts: Date.now(),
    seq: wsCounter++,
    protocol: 'WebSocket',
  };
  const msg = JSON.stringify(payload);
  
  // Use simulated latency
  const { min, max } = networkSimulation.latency;
  const networkDelay = Math.random() * (max - min) + min;
  
  setTimeout(() => {
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        try {
          client.send(msg);
          messagesSent++;
        } catch (err) {
          console.log('💥 WebSocket send error:', err.message);
        }
      }
    });
  }, networkDelay);
}, 1000);

wss.on('connection', ws => {
  wsClients++;
  console.log(`✅ WS connected. Total: ${wsClients}`);
  
  // Send immediate connection confirmation
  ws.send(JSON.stringify({
    type: 'connected',
    ts: Date.now(),
    protocol: 'WebSocket'
  }));
  
  ws.on('close', (code, reason) => {
    wsClients = Math.max(0, wsClients - 1);
    console.log(`❌ WS disconnected (${code}). Total: ${wsClients}`);
  });
  
  ws.on('error', (err) => {
    wsClients = Math.max(0, wsClients - 1);
    console.log(`💥 WS error: ${err.message}. Total: ${wsClients}`);
  });
  
  // Heartbeat to detect dead connections
  ws.isAlive = true;
  ws.on('pong', () => {
    ws.isAlive = true;
  });
});/**
 * Start server
 */
// Heartbeat to clean up dead WebSocket connections
setInterval(() => {
  wss.clients.forEach(ws => {
    if (!ws.isAlive) {
      wsClients = Math.max(0, wsClients - 1);
      console.log(`💀 WS dead connection removed. Total: ${wsClients}`);
      return ws.terminate();
    }
    ws.isAlive = false;
    ws.ping();
  });
}, 30000); // Check every 30 seconds

server.listen(3000, () => {
  console.log('🚀 Server running at http://localhost:3000');
  console.log('📍 SSE Endpoint: http://localhost:3000/sse');
  console.log('📍 WebSocket Endpoint: ws://localhost:3000/ws');
  console.log('📍 Dashboard: http://localhost:3000');
});