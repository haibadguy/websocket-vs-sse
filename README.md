# SSE vs WebSocket Performance Comparison

So sánh hiệu suất thời gian thực giữa Server-Sent Events và WebSocket với dashboard trực quan và metrics chi tiết.

## So sánh những gì?

### 1. Latency (Độ trễ)
- **SSE**: HTTP-based, overhead lớn hơn
- **WebSocket**: Binary protocol, overhead nhỏ hơn
- **Đo lường**: Thời gian từ server gửi đến client nhận (timestamp diff)

### 2. Connection Management
- **SSE**: Tự động reconnect, đơn giản hơn
- **WebSocket**: Cần xử lý reconnection manually
- **Theo dõi**: Số client đang kết nối real-time

### 3. Protocol Overhead
- **SSE**: ~87 bytes/message (HTTP headers)
- **WebSocket**: ~14 bytes/message (frame headers)
- **Impact**: Ảnh hưởng đến bandwidth và performance

### 4. Browser Support
- **SSE**: Hỗ trợ rộng rãi, fallback tốt
- **WebSocket**: Cần polyfill cho browser cũ

## Cách chạy

### Node.js Server (Khuyên dùng)
```bash
npm install
node server.js
```
→ Mở `http://localhost:3000`

### Flask Server (SSE only)
```bash
pip install -r requirements.txt
python flask_server.py
```
→ Mở `http://localhost:5000`

### FastAPI Server (SSE only)
```bash
pip install -r requirements.txt
python fastapi_server.py
```
→ Mở `http://localhost:8000`

## Cách xem so sánh

### 1. Dashboard Web
- **Metrics real-time**: Messages, latency, sequence numbers
- **Server stats**: Client count, uptime, total messages
- **Performance summary**: Protocol nào nhanh hơn và chênh lệch bao nhiêu

### 2. Console Logging
Mở **Developer Tools (F12)** → **Console** để xem:

```javascript
// SSE events
SSE: Connecting to /sse...
SSE: Connection opened
SSE: Received data: {"ts":1703847892123,"seq":5,"protocol":"SSE"}

// WebSocket events  
WebSocket: Connecting to ws://localhost:3000/ws
WebSocket: Connected successfully
WebSocket: Received: {"ts":1703847892124,"seq":5,"protocol":"WebSocket"}
```

### 3. Server Terminal
```
Server running on http://localhost:3000
SSE client connected. Total: 1
WebSocket client connected. Total: 1
SSE client disconnected. Total: 0
```

### 4. Network Tab Analysis
- **SSE**: Xem trong tab "EventStream" 
- **WebSocket**: Xem trong tab "WS" frames
- **Headers**: So sánh overhead của từng request

## Kết quả thường thấy

**Latency**: WebSocket thắng ~10-30ms
**Simplicity**: SSE thắng (ít code hơn)
**Bidirectional**: WebSocket thắng
**Fallback**: SSE thắng (HTTP-based)

## File structure
```
├── server.js          # Node.js (SSE + WebSocket)
├── flask_server.py    # Python Flask (SSE only)  
├── fastapi_server.py  # Python FastAPI (SSE only)
├── public/index.html  # Dashboard comparison
└── requirements.txt   # Python dependencies
```
