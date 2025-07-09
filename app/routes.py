from flask import request, jsonify, redirect
from app.models import get_short_url, find_original_url

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/', methods=['GET'])
    def home():
        """Health check endpoint"""
        return jsonify({"message": "URL Shortener API is running!"})
    
    #POST /shorten - takes in a long URL and returns a short URL
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        original_url = request.json.get('url')
        short_url = get_short_url(original_url)
        short_url = f"{request.url_root.rstrip('/')}/{short_url}"
        return jsonify({'short_url': short_url})

    #GET /<short_url> - redirects to the original long URL
    @app.route('/<short_url>', methods=['GET'])
    def redirect_to_url(short_url):
        original_url = find_original_url(short_url)
        if original_url:
            return redirect(original_url)
        return jsonify({'error': 'URL not found'}), 404

    #GET /decode/<short_url> - decodes the short URL to return the original long URL
    @app.route('/decode/<short_url>', methods=['GET'])
    def decode_url(short_url):
        original_url = find_original_url(short_url)
        if original_url:
            return jsonify({'original_url': original_url})
        return jsonify({'error': 'URL not found'}), 404
