#!/bin/bash

# URL Shortener Production Build Script
# This script builds the React frontend for production

echo "🏗️  Building URL Shortener for Production"
echo "========================================="

# Build the React frontend
echo "Building React frontend..."
cd frontend
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully!"
    echo "📦 Build files are in frontend/build/"
    echo ""
    echo "🚀 To serve the production build:"
    echo "   Option 1: Use a static file server"
    echo "   npm install -g serve"
    echo "   serve -s frontend/build -l 3000"
    echo ""
    echo "   Option 2: Use Python's built-in server"
    echo "   cd frontend/build && python -m http.server 3000"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
