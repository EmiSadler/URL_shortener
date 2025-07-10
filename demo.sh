#!/bin/bash

# URL Shortener Demo Script
# This script demonstrates the functionality of the URL shortener

echo "🎬 URL Shortener Demo"
echo "===================="
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ Backend is not running. Please start it first:"
    echo "   python main.py"
    echo ""
    exit 1
fi

echo "✅ Backend is running!"
echo ""

# Demo URLs to shorten
URLS=(
    "https://www.google.com"
    "https://github.com"
    "https://stackoverflow.com"
    "https://www.youtube.com"
)

echo "📋 Demonstrating URL shortening:"
echo ""

SHORT_URLS=()

for url in "${URLS[@]}"; do
    echo "🔗 Shortening: $url"
    
    # Call the API to shorten the URL
    response=$(curl -s -X POST http://localhost:8000/shorten \
        -H "Content-Type: application/json" \
        -d "{\"url\": \"$url\"}")
    
    # Extract the short URL from the response
    short_url=$(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['short_url'])")
    
    echo "   ➡️  $short_url"
    echo ""
    
    SHORT_URLS+=("$short_url")
done

echo "🔍 Testing redirects:"
echo ""

for short_url in "${SHORT_URLS[@]}"; do
    echo "Testing: $short_url"
    
    # Get the redirect location
    redirect_url=$(curl -s -I "$short_url" | grep -i location | cut -d' ' -f2 | tr -d '\r')
    
    echo "   ↪️  Redirects to: $redirect_url"
    echo ""
done

echo "📊 Testing decode functionality:"
echo ""

for short_url in "${SHORT_URLS[@]}"; do
    # Extract just the short code from the URL
    short_code=$(basename "$short_url")
    
    echo "Decoding: $short_code"
    
    # Call the decode API
    response=$(curl -s "http://localhost:8000/decode/$short_code")
    original_url=$(echo $response | python3 -c "import sys, json; print(json.load(sys.stdin)['original_url'])")
    
    echo "   🔍 Original URL: $original_url"
    echo ""
done

echo "🎉 Demo completed!"
echo ""
echo "💡 Try the web interface at: http://localhost:3000"
echo ""
echo "📚 API endpoints:"
echo "   GET  /              - Health check"
echo "   POST /shorten       - Shorten a URL"
echo "   GET  /{short_code}  - Redirect to original URL"
echo "   GET  /decode/{code} - Get original URL without redirect"
