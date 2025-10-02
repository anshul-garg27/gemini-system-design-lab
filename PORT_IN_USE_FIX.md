# Fix: Address Already in Use (Port 8000)

## 🐛 **Error**

```
ERROR: [Errno 48] Address already in use
```

## 🔍 **Cause**

Port 8000 पहले से use में है - पुराना server process चल रहा है जो properly stop नहीं हुआ था।

## ✅ **Solution**

### Quick Fix (One Command):
```bash
# Kill all processes using port 8000 and restart
lsof -ti:8000 | xargs kill -9 && python3 start_unified_server.py
```

### Step-by-Step Fix:

#### 1. Find processes using port 8000:
```bash
lsof -ti:8000
```

**Output:**
```
13278
20308
88530
```

#### 2. Kill those processes:
```bash
kill -9 13278 20308 88530
```

Or kill all at once:
```bash
kill -9 $(lsof -ti:8000)
```

#### 3. Restart server:
```bash
python3 start_unified_server.py
```

## 🔧 **Alternative Ports**

If you want to use a different port:

### Option 1: Change in code
Edit `start_unified_server.py`:
```python
# Change this line:
uvicorn.run(app, host="0.0.0.0", port=8000, ...)

# To:
uvicorn.run(app, host="0.0.0.0", port=8001, ...)
```

### Option 2: Run with different port
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 📊 **Check What's Using Ports**

### Check specific port:
```bash
lsof -i:8000
```

**Output:**
```
COMMAND   PID     USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python    13278   user   3u   IPv4 0x1234567890      0t0  TCP *:8000 (LISTEN)
```

### Check all Python processes:
```bash
ps aux | grep python
```

### Check FastAPI/Uvicorn processes:
```bash
ps aux | grep uvicorn
```

## 🛑 **Properly Stop Server**

To avoid this issue in future:

### If running in terminal:
```bash
# Press Ctrl+C to stop
^C
```

### If running in background:
```bash
# Find PID
ps aux | grep "start_unified_server"

# Kill gracefully
kill <PID>

# Or force kill
kill -9 <PID>
```

## 🚀 **Recommended Workflow**

### Terminal 1: Backend Server
```bash
cd /Users/a0g11b6/Desktop/InterviewPrep/SysDesignGemini
source venv/bin/activate
python3 start_unified_server.py

# To stop: Ctrl+C
```

### Terminal 2: Worker Service
```bash
cd /Users/a0g11b6/Desktop/InterviewPrep/SysDesignGemini
source venv/bin/activate
python3 -m app.worker_service

# To stop: Ctrl+C
```

### Terminal 3: Frontend (if needed)
```bash
cd /Users/a0g11b6/Desktop/InterviewPrep/SysDesignGemini/frontend
npm run dev

# To stop: Ctrl+C
```

## 🔍 **Debugging Commands**

### Check if port is free:
```bash
nc -zv localhost 8000
# Output: "Connection refused" = Port is free ✅
# Output: "succeeded!" = Port is in use ❌
```

### Check all listening ports:
```bash
lsof -iTCP -sTCP:LISTEN -n -P
```

### Find process by port:
```bash
lsof -i:8000 -P -n
```

## 📝 **Common Scenarios**

### Scenario 1: Server crashed but process still running
```bash
# Solution:
kill -9 $(lsof -ti:8000)
python3 start_unified_server.py
```

### Scenario 2: Multiple servers accidentally started
```bash
# Check how many:
lsof -ti:8000 | wc -l

# Kill all:
lsof -ti:8000 | xargs kill -9

# Restart one:
python3 start_unified_server.py
```

### Scenario 3: Port conflict with another app
```bash
# Option 1: Stop other app
# Option 2: Use different port (see above)
# Option 3: Find what's using it:
lsof -i:8000
```

## 🎯 **Prevention**

### Use a cleanup script:
Create `stop_all.sh`:
```bash
#!/bin/bash

echo "Stopping all services..."

# Kill server
echo "Stopping FastAPI server..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "  No server on port 8000"

# Kill worker
echo "Stopping worker service..."
pkill -f "worker_service" 2>/dev/null || echo "  No worker service running"

echo "✅ All services stopped!"
```

Make executable:
```bash
chmod +x stop_all.sh
```

Use:
```bash
./stop_all.sh
```

## ✅ **Current Status**

**Fixed!** Old processes killed:
```
✅ Killed PID 13278
✅ Killed PID 20308
✅ Killed PID 88530
```

**Now you can start fresh:**
```bash
python3 start_unified_server.py
```

## 🎉 **Summary**

**Problem:** Port 8000 already in use
**Cause:** Old server processes not stopped properly
**Solution:** Kill old processes and restart

**Quick Command:**
```bash
kill -9 $(lsof -ti:8000) && python3 start_unified_server.py
```

**Port is now free!** 🚀
