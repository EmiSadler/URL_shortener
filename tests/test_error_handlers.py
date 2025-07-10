import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.error_handlers import (
    handle_server_error, 
    handle_not_found, 
    create_success_response, 
    create_error_response
)


class TestErrorHandlers:
    # Test error handling functions

    def setup_method(self):
        # Setup test Flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
    
    def test_handle_server_error(self):
        # Test server error handler
        with self.app.app_context():
            error = Exception("Test error")
            response, status_code = handle_server_error(error, "test context")
            
            assert status_code == 500
            assert response.is_json
            
            # Test the JSON response
            json_data = response.get_json()
            assert 'error' in json_data
            assert 'Internal server error occurred test context' in json_data['error']
    
    def test_handle_server_error_no_context(self):
        # Test server error handler without context
        with self.app.app_context():
            error = Exception("Test error")
            response, status_code = handle_server_error(error)
            
            assert status_code == 500
            json_data = response.get_json()
            assert json_data['error'] == 'Internal server error occurred'
    
    @patch('app.error_handlers.logger')
    def test_handle_server_error_logging(self, mock_logger):
        # Test that server errors are logged
        with self.app.app_context():
            error = Exception("Test error")
            handle_server_error(error, "test context")
            
            mock_logger.error.assert_called_once()
            logged_message = mock_logger.error.call_args[0][0]
            assert "Server error in test context: Test error" in logged_message
    
    def test_handle_not_found_default(self):
        # Test not found handler with default parameters
        with self.app.app_context():
            response, status_code = handle_not_found()
            
            assert status_code == 404
            json_data = response.get_json()
            assert json_data['error'] == 'Short URL not found'
    
    def test_handle_not_found_custom_resource(self):
        # Test not found handler with custom resource type
        with self.app.app_context():
            response, status_code = handle_not_found("Custom Resource", "test123")
            
            assert status_code == 404
            json_data = response.get_json()
            assert json_data['error'] == 'Custom Resource not found'
            assert json_data['custom_resource'] == 'test123'
    
    def test_handle_not_found_with_id(self):
        # Test not found handler with resource ID
        with self.app.app_context():
            response, status_code = handle_not_found("Short URL", "abc123")
            
            assert status_code == 404
            json_data = response.get_json()
            assert json_data['error'] == 'Short URL not found'
            assert json_data['short_url'] == 'abc123'
    
    def test_create_success_response_default(self):
        # Test success response with default status code
        with self.app.app_context():
            data = {'message': 'Success'}
            response, status_code = create_success_response(data)
            
            assert status_code == 200
            assert response.is_json
            json_data = response.get_json()
            assert json_data['message'] == 'Success'
    
    def test_create_success_response_custom_status(self):
        # Test success response with custom status code
        with self.app.app_context():
            data = {'created': True}
            response, status_code = create_success_response(data, 201)
            
            assert status_code == 201
            json_data = response.get_json()
            assert json_data['created'] == True
    
    def test_create_error_response(self):
        # Test error response creation
        with self.app.app_context():
            error_dict = {'error': 'Validation failed'}
            response, status_code = create_error_response(error_dict, 400)
            
            assert status_code == 400
            assert response.is_json
            json_data = response.get_json()
            assert json_data['error'] == 'Validation failed'
    
    def test_create_error_response_complex(self):
        # Test error response with complex error data
        with self.app.app_context():
            error_dict = {
                'error': 'Validation failed',
                'field': 'url',
                'code': 'INVALID_FORMAT'
            }
            response, status_code = create_error_response(error_dict, 422)
            
            assert status_code == 422
            json_data = response.get_json()
            assert json_data['error'] == 'Validation failed'
            assert json_data['field'] == 'url'
            assert json_data['code'] == 'INVALID_FORMAT'
