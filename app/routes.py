from flask import request, jsonify, redirect
from app.models import get_short_url, find_original_url
import re

def is_valid_url(url):
    """Basic URL validation"""
    if not url or not isinstance(url, str):
        return False
    
    # Check if URL starts with http:// or https://
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

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
    
            # Check if JSON body exists
            if request.json is None:
                return jsonify({
                    'error': 'Request body must contain valid JSON'
                }), 400
            
            # Check if 'url' field exists
            if 'url' not in request.json:
                return jsonify({
                    'error': 'Missing required field: url'
                }), 400
            
            original_url = request.json.get('url')
            
            # Check if URL is empty or None
            if not original_url or not original_url.strip():
                return jsonify({
                    'error': 'URL cannot be empty'
                }), 400
            
            # Validate URL format
            if not is_valid_url(original_url.strip()):
                return jsonify({
                    'error': 'Invalid URL format. URL must start with http:// or https://'
                }), 422  # Unprocessable Entity
            
            # Check URL length (reasonable limit)
            if len(original_url) > 2048:
                return jsonify({
                    'error': 'URL too long. Maximum length is 2048 characters'
                }), 422
            
            # Generate short URL
            short_url = get_short_url(original_url.strip())
            full_short_url = f"{request.url_root.rstrip('/')}/{short_url}"
            
            return jsonify({
                'short_url': full_short_url,
                'original_url': original_url.strip()
            }), 201  # Created
            
        except Exception as e:
            # Log the error in production you'd use proper logging
            print(f"Error in shorten_url: {str(e)}")
            return jsonify({
                'error': 'Internal server error occurred while creating short URL'
            }), 500

    #GET /<short_url> - redirects to the original long URL
    @app.route('/<short_url>', methods=['GET'])
    def redirect_to_url(short_url):
        try:
            # Basic validation of short_url format
            if not short_url or len(short_url.strip()) == 0:
                return jsonify({
                    'error': 'Invalid short URL format'
                }), 400
            
            # Check for reasonable length (base62 shouldn't be too long)
            if len(short_url) > 10:  # Adjust based on your needs
                return jsonify({
                    'error': 'Invalid short URL format'
                }), 400
                
            original_url = find_original_url(short_url.strip())
            
            if original_url:
                return redirect(original_url), 302  # Found - Temporary Redirect
            else:
                return jsonify({
                    'error': 'Short URL not found',
                    'short_url': short_url
                }), 404  # Not Found
                
        except Exception as e:
            print(f"Error in redirect_to_url: {str(e)}")
            return jsonify({
                'error': 'Internal server error occurred during redirect'
            }), 500

    #GET /decode/<short_url> - decodes the short URL to return the original long URL
    @app.route('/decode/<short_url>', methods=['GET'])
    def decode_url(short_url):
        try:
            # Basic validation of short_url format
            if not short_url or len(short_url.strip()) == 0:
                return jsonify({
                    'error': 'Invalid short URL format'
                }), 400
            
            # Check for reasonable length
            if len(short_url) > 10:
                return jsonify({
                    'error': 'Invalid short URL format'
                }), 400
                
            original_url = find_original_url(short_url.strip())
            
            if original_url:
                return jsonify({
                    'original_url': original_url,
                    'short_url': short_url
                }), 200  # OK
            else:
                return jsonify({
                    'error': 'Short URL not found',
                    'short_url': short_url
                }), 404  # Not Found
                
        except Exception as e:
            print(f"Error in decode_url: {str(e)}")
            return jsonify({
                'error': 'Internal server error occurred during decode'
            }), 500
