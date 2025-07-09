from flask import request, jsonify, redirect, url_for
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
    def home():
        """Health check endpoint"""
        return jsonify({"message": "URL Shortener API is running!"})
    
    #POST /shorten - takes in a long URL and returns a short URL
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        try:
            # Validate the request
            is_valid, error_response, status_code = validate_shorten_request(
                request.json, request.is_json
            )
            
            if not is_valid:
                return create_error_response(error_response, status_code)
            
            # Generate short URL
            original_url = request.json.get('url').strip()
            short_url = get_short_url(original_url)
            full_short_url = url_for('redirect_to_url', short_url=short_url, _external=True)
            
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

    #GET /decode/<short_url> - decodes the short URL to return the original long URL
    @app.route('/decode/<short_url>', methods=['GET'])
    def decode_url(short_url):
        try:
            # Validate short URL format
            is_valid, error_response, status_code = validate_short_url(short_url)
            
            if not is_valid:
                return create_error_response(error_response, status_code)
                
            original_url = find_original_url(short_url.strip())
            
            if original_url:
                return create_success_response({
                    'original_url': original_url,
                    'short_url': short_url
                })
            else:
                return handle_not_found("Short URL", short_url)
                
        except Exception as e:
            return handle_server_error(e, "during decode")
