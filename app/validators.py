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

def validate_shorten_request(request_data, is_json):
    """
    Validate the /shorten endpoint request
    Returns: (is_valid, error_response, status_code)
    """
    # Check if request has JSON content
    if not is_json:
        return False, {'error': 'Content-Type must be application/json'}, 400
    
    # Check if JSON body exists
    if request_data is None:
        return False, {'error': 'Request body must contain valid JSON'}, 400
    
    # Check if 'url' field exists
    if 'url' not in request_data:
        return False, {'error': 'Missing required field: url'}, 400
    
    original_url = request_data.get('url')
    
    # Check if URL is empty or None
    if not original_url or not original_url.strip():
        return False, {'error': 'URL cannot be empty'}, 400
    
    # Validate URL format
    if not is_valid_url(original_url.strip()):
        return False, {
            'error': 'Invalid URL format. URL must start with http:// or https://'
        }, 422
    
    # Check URL length (reasonable limit)
    if len(original_url) > MAX_URL_LENGTH:
        return False, {
            f'error': f'URL too long. Maximum length is {MAX_URL_LENGTH} characters'
        }, 422
    
    return True, None, None

def validate_short_url(short_url):
    """
    Validate short URL format
    Returns: (is_valid, error_response, status_code)
    """
    # Basic validation of short_url format
    if not short_url or len(short_url.strip()) == 0:
        return False, {'error': 'Invalid short URL format'}, 400
    
    # Check for reasonable length (base62 shouldn't be too long)
    if len(short_url) > 10:
        return False, {'error': 'Invalid short URL format'}, 400
    
    return True, None, None
