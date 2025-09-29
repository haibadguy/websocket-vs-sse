# WebSocket vs Server-Sent Events (SSE) - Performance Comparison

**Tiêu điểm công nghệ**: Triển khai SSE, quản lý kết nối, giải pháp dự phòng  
**Demo**: Bảng điều khiển thời gian thực so sánh SSE và WebSocket  
**Đổi mới**: Giao tiếp thời gian thực nhẹ nhàng  
**Ngôn ngữ**: Node.js, Python Flask/FastAPI  

---

## 📋 Tổng quan dự án

Dự án này thực hiện **so sánh hiệu suất chi tiết** giữa hai công nghệ real-time communication:
- **Server-Sent Events (SSE)**: HTTP-based, unidirectional
- **WebSocket**: Binary protocol, bidirectional

### 🎯 Mục tiêu kỹ thuật
1. **Đo lường latency** chính xác với timestamp synchronization
2. **Phân tích protocol overhead** và bandwidth usage
3. **Test connection management** và reconnection handling  
4. **So sánh throughput** trong điều kiện mạng khác nhau
5. **Đánh giá resource usage** (CPU, memory) của client/server

---

## 🔬 Các chỉ số so sánh

### 1. 📊 Latency (Độ trễ)
```javascript
// Cách đo latency
const latency = Date.now() - data.timestamp;
// Validation để tránh kết quả sai
if (latency < 0 || latency > 10000) return;
```

**Kết quả thường thấy:**
- **SSE**: 15-45ms (HTTP overhead)
- **WebSocket**: 10-35ms (binary protocol)

### 2. 🚀 Throughput (Tần suất)
```javascript
// Đếm messages per second
const messagesPerSecond = messageCount / timeElapsed;
```

### 3. 🏋️ Protocol Overhead
- **SSE**: ~87 bytes/message (HTTP headers + event format)
- **WebSocket**: ~14 bytes/message (frame headers only)

### 4. 🔗 Connection Management
```javascript
// SSE - Tự động reconnect
eventSource.onerror = () => setTimeout(reconnect, 3000);

// WebSocket - Manual reconnect
websocket.onclose = () => setTimeout(reconnect, 3000);
```

### 5. 💻 Resource Usage
- Browser DevTools monitoring
- Memory usage tracking
- CPU performance impact

### 6. 🌐 Multi-client Load
```bash
# Test với nhiều client đồng thời
for i in {1..10}; do
    open http://localhost:3000 &
done
```

---

## 🚀 Hướng dẫn cài đặt & chạy

### Prerequisites
```bash
# Node.js version 14+
node --version

# Python 3.8+ (cho Flask/FastAPI servers)
python --version
```

### 1. Node.js Server (Chính)
```bash
# Clone repository
git clone <repository-url>
cd websocket-vs-sse

# Install dependencies
npm install

# Start server
node server.js
```
**Truy cập**: http://localhost:3000

### 2. Flask Server (SSE Only)
```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python flask_server.py
```
**Truy cập**: http://localhost:5000

### 3. FastAPI Server (SSE Only)
```bash
# Cùng virtual environment
pip install -r requirements.txt

# Start FastAPI server
python fastapi_server.py
```
**Truy cập**: http://localhost:8000

---

## 📊 Cách sử dụng Dashboard

### Interface chính
1. **Connection Status**: Trạng thái kết nối real-time
2. **Metrics Display**: Latency, throughput, message count
3. **Network Simulation**: Test với network conditions khác nhau
4. **Performance Comparison**: Tự động so sánh và hiển thị winner

### Controls
```html
<!-- Network Simulation -->
<button onclick="simulateNetworkIssue()">Simulate Network Issue</button>
<button onclick="restoreNetwork()">Restore Network</button>

<!-- Load Testing -->
<button onclick="window.open(location.href)">Open New Client</button>
```

### Real-time Metrics
```javascript
// Auto-update mỗi giây
setInterval(updateMetrics, 1000);

function updateMetrics() {
    // Calculate average latency
    // Update throughput counters  
    // Compare protocols
    // Display winner
}
```

---

## 🔍 Cách theo dõi & debug

### 1. Dashboard Web (Primary)
- **Live metrics**: Latency, throughput, connection count
- **Visual comparison**: Progress bars và charts
- **Winner analysis**: Tự động tính toán protocol nào tốt hơn

### 2. Browser Console (F12)
```javascript
// SSE Debug logs
console.log('📡 SSE: Connecting to /sse...');
console.log('📡 SSE: Message received:', data);
console.log('📡 SSE: Latency:', latency + 'ms');

// WebSocket Debug logs  
console.log('🔌 WebSocket: Connecting...');
console.log('🔌 WebSocket: Message received:', data);
console.log('🔌 WebSocket: Latency:', latency + 'ms');

// Performance comparison
console.log('🏆 WebSocket is faster by', diff + 'ms', '(' + percentage + '%)');
```

### 3. Server Terminal
```bash
# Connection tracking
📡 SSE client connected. Total: 1
🔌 WebSocket client connected. Total: 1

# Message broadcasting  
📡 SSE: Broadcasting message 1 to 1 clients
🔌 WS: Broadcasting message 1 to 1 clients

# Disconnection handling
💀 SSE client disconnected. Total: 0
💀 WS client disconnected. Total: 0
```

### 4. Network Tab Analysis
- **SSE**: Event-stream requests, HTTP headers
- **WebSocket**: WS frames, binary data
- **Size comparison**: Payload + overhead analysis

---

## 🧪 Testing Scenarios

### 1. Normal Conditions
```javascript
// Expected results
SSE: 20-40ms average latency
WebSocket: 15-30ms average latency
Winner: WebSocket (25-35% faster)
```

### 2. Network Issues
```javascript
// Simulate packet loss
simulateNetworkIssue();
// SSE: Auto-reconnects after 3s
// WebSocket: Manual reconnect required
```

### 3. High Load Testing
```bash
# Open multiple tabs
for i in {1..20}; do open http://localhost:3000; done

# Monitor server performance
htop  # CPU usage
netstat -an | grep :3000  # Connection count
```

### 4. Cross-platform Testing
```bash
# Test all 3 servers simultaneously
node server.js &          # Port 3000
python flask_server.py &  # Port 5000  
python fastapi_server.py & # Port 8000
```

---

## 📂 Cấu trúc dự án

```
websocket-vs-sse/
├── 📄 server.js              # Node.js server (SSE + WebSocket + API)
├── 📄 flask_server.py        # Flask SSE implementation
├── 📄 fastapi_server.py      # FastAPI SSE implementation
├── 📄 requirements.txt       # Python dependencies
├── 📄 package.json           # Node.js dependencies  
├── 📁 public/
│   └── 📄 index.html         # Dashboard comparison UI
└── 📄 README.md              # Documentation (this file)
```

### Key Files Breakdown

#### `server.js` (213 lines)
```javascript
// Core features
- Express server với CORS support
- SSE endpoint: /sse với proper headers
- WebSocket endpoint: /ws với connection tracking
- API endpoints: /api/stats, /api/simulate-network
- Heartbeat mechanism (30s intervals)
- Network simulation capabilities
- Real-time client counting
```

#### `public/index.html` (585 lines)  
```html
<!-- Key components -->
- Real-time metrics dashboard
- SSE và WebSocket connection handlers
- Network simulation controls
- Performance comparison logic
- Responsive design với CSS Grid
- Console logging cho debugging
```

#### `flask_server.py` & `fastapi_server.py`
```python
# Features
- SSE streaming endpoints
- CORS handling
- JSON response format
- Sequence number tracking  
- Error handling và logging
```

---

## 🎯 Kết quả benchmark thường thấy

### Performance Comparison

| Tiêu chí | SSE | WebSocket | Winner |
|----------|-----|-----------|--------|
| **Latency** | 20-40ms | 15-30ms | 🏆 WebSocket |
| **Overhead** | ~87 bytes | ~14 bytes | 🏆 WebSocket |
| **Simplicity** | ✅ Auto-reconnect | ❌ Manual handling | 🏆 SSE |
| **Bidirectional** | ❌ Unidirectional | ✅ Full-duplex | 🏆 WebSocket |
| **HTTP Caching** | ✅ Standard HTTP | ❌ No caching | 🏆 SSE |
| **Firewall/Proxy** | ✅ HTTP-friendly | ❌ May be blocked | 🏆 SSE |

### Use Case Recommendations

**Choose SSE when:**
- Simple server-to-client updates
- Need automatic reconnection  
- HTTP infrastructure requirements
- Live feeds, notifications, monitoring

**Choose WebSocket when:**
- Bidirectional communication needed
- Low latency critical (gaming, trading)
- High message frequency
- Binary data transfer

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Cannot GET /" Error
```bash
# Solution: Check if server is running
node server.js
# Should see: "Server running on http://localhost:3000"
```

#### 2. SSE Connection Fails
```javascript
// Check browser console for CORS errors
// Ensure proper headers in server response
res.setHeader('Access-Control-Allow-Origin', '*');
```

#### 3. WebSocket Connection Refused
```bash
# Check if port is already in use
netstat -an | grep 3000
# Kill existing process if needed
pkill -f "node server.js"
```

#### 4. Negative Latency Values
```javascript
// Cause: Clock synchronization issues
// Solution: Added validation in code
if (latency < 0 || latency > 10000) {
    console.warn('Invalid latency:', latency);
    return;
}
```

#### 5. Network Simulation Not Working
```javascript
// DevTools throttling doesn't affect localhost
// Use built-in network simulation instead
simulateNetworkIssue(); // Custom implementation
```

---

## 🔧 Advanced Configuration

### Custom Latency Simulation
```javascript
// In server.js - add realistic delays
const simulatedDelay = Math.random() * 30 + 10; // 10-40ms
setTimeout(() => {
    // Send response
}, simulatedDelay);
```

### Multi-server Load Balancing
```bash
# Run multiple instances
node server.js --port 3000 &
node server.js --port 3001 &
node server.js --port 3002 &

# Use nginx for load balancing
upstream backend {
    server localhost:3000;
    server localhost:3001;
    server localhost:3002;
}
```

### Performance Monitoring
```javascript
// Add to client code
const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        console.log('Performance:', entry);
    }
});
observer.observe({entryTypes: ['navigation', 'resource']});
```

---

## 📜 License & Credits

**License**: MIT © 2025  
**Author**: haibadguy  
**Tech Focus**: SSE implementation, connection management, fallbacks  
**Innovation**: Lightweight real-time communication comparison  

### Dependencies
```json
{
  "express": "^4.18.2",
  "cors": "^2.8.5", 
  "express-ws": "^5.0.2",
  "flask": "^2.3.3",
  "fastapi": "^0.104.1",
  "uvicorn": "^0.24.0"
}
```

---

**🎯 Key Takeaway**: Dự án này không chỉ so sánh performance mà còn demonstate các best practices trong việc implement real-time communication, handle connection issues, và optimize cho production environment.
