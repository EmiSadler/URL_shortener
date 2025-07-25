from flask import request, jsonify, redirect, url_for, send_from_directory
import os
from app.models import get_short_url, find_original_url
from app.validators import validate_shorten_request, validate_short_url
from app.error_handlers import (
    handle_server_error, 
    handle_not_found, 
    create_success_response, 
    create_error_response
)

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/', methods=['GET'])
    def serve_frontend():
        """Serve the React frontend index.html"""
        # Use different static folder path for local vs Docker
        if os.path.exists('/app/static'):
            static_folder = '/app/static'  # Docker path
        else:
            # For local development, return a simple response instead of trying to serve files
            return jsonify({"message": "URL Shortener API is running!", "frontend": "available at localhost:3000"})

    
    #POST /shorten - takes in a long URL and returns a short URL
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        try:
            # Handle Flask's JSON parsing errors
            if not request.is_json:
                return create_error_response(
                    {'error': 'Content-Type must be application/json'}, 400
                )
            
            # Try to access request.json to trigger any JSON parsing errors
            try:
                request_data = request.json
            except Exception:
                return create_error_response(
                    {'error': 'Request body must contain valid JSON'}, 400
                )
            
            # Validate the request
            is_valid, error_response, status_code = validate_shorten_request(
                request_data, request.is_json
            )
            
            if not is_valid:
                return create_error_response(error_response, status_code)
            
            # Generate short URL
            original_url = request_data.get('url').strip()
            short_url = get_short_url(original_url)
            
            # Use HTTPS if the request came from HTTPS
            scheme = 'https' if request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https' else 'http'
            
            try:
                full_short_url = url_for('redirect_to_url', short_url=short_url, _external=True, _scheme=scheme)
            except Exception as e:
                # Fallback for local development
                print(f"url_for failed: {e}")
                host = request.headers.get('Host', 'localhost:8000')
                full_short_url = f"{scheme}://{host}/{short_url}"
            
            return create_success_response({
                'short_url': full_short_url,
                'original_url': original_url
            }, 201)
            
        except Exception as e:
            return handle_server_error(e, "while creating short URL")

    #GET /<short_url> - redirects to the original long URL
    @app.route('/<short_url>', methods=['GET'])
    def redirect_to_url(short_url):
        try:
            # Validate short URL format
            is_valid, error_response, status_code = validate_short_url(short_url)
            
            if not is_valid:
                return create_error_response(error_response, status_code)
                
            original_url = find_original_url(short_url.strip())
            
            if original_url:
                return redirect(original_url), 302  # Found - Temporary Redirect
            else:
                return handle_not_found("Short URL", short_url)
                
        except Exception as e:
            return handle_server_error(e, "during redirect")

