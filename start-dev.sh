#!/bin/bash

# URL Shortener Development Startup Script
# This script starts both the Flask backend and React frontend in development mode

echo "🚀 Starting URL Shortener Development Environment"
echo "================================================"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    fi
    return 0
}

# Check if ports are available
if ! check_port 8000; then
    echo "❌ Backend port 8000 is in use. Please free it and try again."
    exit 1
fi

if ! check_port 3000; then
    echo "❌ Frontend port 3000 is in use. Please free it and try again."
    exit 1
fi

# Create log directory
mkdir -p logs

echo "📦 Installing/updating dependencies..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > logs/pip-install.log 2>&1

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install > ../logs/npm-install.log 2>&1
cd ..

echo "🔧 Starting Backend (Flask) on port 8000..."
python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! check_port 8000; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start. Check logs/backend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "⚛️  Starting Frontend (React) on port 3000..."
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

echo ""
echo "🎉 Development environment started successfully!"
echo ""
echo "📍 Application URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "📋 Available endpoints:"
echo "   GET  / - Health check"
echo "   POST /shorten - Shorten a URL"
echo "   GET  /{short_url} - Redirect to original URL"
echo ""
echo "📝 Logs are available in the logs/ directory"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Register cleanup function to run on script exit
trap cleanup SIGINT SIGTERM

# Keep script running
echo "Press Ctrl+C to stop both servers"
wait
