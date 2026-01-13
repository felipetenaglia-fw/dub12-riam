#!/bin/bash

# RIAM LMS - Stop Script
# This script stops both the API and UI

echo "🛑 Stopping RIAM LMS services..."

# Read PIDs from files
if [ -f .api.pid ]; then
    API_PID=$(cat .api.pid)
    if kill -0 $API_PID 2>/dev/null; then
        kill $API_PID
        echo "✅ API stopped"
    fi
    rm .api.pid
fi

if [ -f .ui.pid ]; then
    UI_PID=$(cat .ui.pid)
    if kill -0 $UI_PID 2>/dev/null; then
        kill $UI_PID
        echo "✅ UI stopped"
    fi
    rm .ui.pid
fi

# Cleanup any remaining processes
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "ui/app.py" 2>/dev/null

echo "✨ All services stopped"
