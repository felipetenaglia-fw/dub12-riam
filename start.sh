#!/bin/bash

# RIAM LMS - Quick Start Script
# This script starts both the API and UI

echo "🎵 RIAM Learning Management System"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "Starting services..."
echo ""

# Check and terminate existing processes on port 8000
echo "🔍 Checking for existing processes on port 8000..."
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "   Found process(es) on port 8000, terminating..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 2
    echo "   ✅ Port 8000 cleared"
fi

# Check and terminate existing processes on port 5001
echo "🔍 Checking for existing processes on port 5001..."
if lsof -ti:5001 > /dev/null 2>&1; then
    echo "   Found process(es) on port 5001, terminating..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 2
    echo "   ✅ Port 5001 cleared"
fi

echo ""

# Start API in background
echo "📡 Starting Backend API on port 8000..."
cd api
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../api.log 2>&1 &
API_PID=$!
cd ..

# Wait for API to start
sleep 5

# Check if API is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo "❌ Failed to start API"
    cat api.log
    exit 1
fi

echo "✅ API started (PID: $API_PID)"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""

# Start UI in background
echo "🌐 Starting Web UI on port 5001..."
cd ui
python3 app.py > ../ui.log 2>&1 &
UI_PID=$!
cd ..

# Wait for UI to start
sleep 3

# Check if UI is running
if ! kill -0 $UI_PID 2>/dev/null; then
    echo "❌ Failed to start UI"
    cat ui.log
    kill $API_PID 2>/dev/null
    exit 1
fi

echo "✅ UI started (PID: $UI_PID)"
echo "   - Web: http://localhost:5001"
echo ""

echo "=================================="
echo "✨ All services are running!"
echo ""
echo "📱 Open http://localhost:5001 in your browser"
echo ""
echo "🔑 Login credentials:"
echo "   - Admin: admin / admin"
echo "   - Teacher: teacher / teacher"
echo "   - Student: student / student"
echo ""
echo "📝 Logs:"
echo "   - API: tail -f api.log"
echo "   - UI: tail -f ui.log"
echo ""
echo "🛑 To stop: ./stop.sh"
echo "   Or manually: kill $API_PID $UI_PID"
echo ""

# Save PIDs for stop script
echo "$API_PID" > .api.pid
echo "$UI_PID" > .ui.pid

# Wait for user interrupt
echo "Press Ctrl+C to stop all services..."
trap "echo ''; echo '🛑 Stopping services...'; kill $API_PID $UI_PID 2>/dev/null; rm -f .api.pid .ui.pid; echo '✅ Services stopped'; exit 0" INT

# Keep script running
wait
