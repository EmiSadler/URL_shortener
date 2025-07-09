from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def handle_server_error(error, context=""):
    """
    Handle server errors consistently
    """
    error_msg = str(error)
    logger.error(f"Server error in {context}: {error_msg}")
    
    return jsonify({
        'error': f'Internal server error occurred{" " + context if context else ""}'
    }), 500

def handle_not_found(resource_type="Short URL", resource_id=""):
    """
    Handle 404 errors consistently
    """
    response = {'error': f'{resource_type} not found'}
    
    if resource_id:
        response[resource_type.lower().replace(' ', '_')] = resource_id
    
    return jsonify(response), 404

def create_success_response(data, status_code=200):
    """
    Create consistent success responses
    """
    return jsonify(data), status_code

def create_error_response(error_dict, status_code):
    """
    Create consistent error responses
    """
    return jsonify(error_dict), status_code
