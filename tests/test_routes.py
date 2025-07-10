import pytest
import json
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from flask import Flask

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.routes import register_routes
from app.db import init_db


class TestRoutes:
    # Test Flask routes
    
    @pytest.fixture
    def app(self):
        # Create a test Flask app
        app = Flask(__name__)
        app.config['TESTING'] = True
        register_routes(app)
        return app
    
    @pytest.fixture
    def client(self, app):
        # Create a test client
        return app.test_client()
    
    @pytest.fixture
    def temp_db(self):
        # Create a temporary database for integration tests
        temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        temp_db_file.close()
        
        with patch('app.db.DB_PATH', temp_db_file.name):
            init_db()
            yield temp_db_file.name
        
        os.unlink(temp_db_file.name)


class TestHealthCheckEndpoint(TestRoutes):
    # Test the health check endpoint

    def test_health_check_success(self, client):
        # Test successful health check
        response = client.get('/')
        
        assert response.status_code == 200
        assert response.is_json
        
        data = response.get_json()
        assert data['message'] == 'URL Shortener API is running!'


class TestShortenEndpoint(TestRoutes):
    # Test the /shorten endpoint

    @patch('app.routes.get_short_url')
    def test_shorten_success(self, mock_get_short_url, client):
        # Test successful URL shortening
        mock_get_short_url.return_value = "abc123"
        
        response = client.post('/shorten', 
                            data=json.dumps({'url': 'https://example.com'}),
                            content_type='application/json')
        
        assert response.status_code == 201
        assert response.is_json
        
        data = response.get_json()
        assert 'short_url' in data
        assert 'original_url' in data
        assert data['original_url'] == 'https://example.com'
        assert 'abc123' in data['short_url']  # Should contain the mocked short code
    
    def test_shorten_invalid_content_type(self, client):
        # Test shorten with invalid content type
        response = client.post('/shorten', 
                            data='{"url": "https://example.com"}',
                            content_type='text/plain')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Content-Type must be application/json'
    
    def test_shorten_missing_url(self, client):
        # Test shorten with missing URL field
        response = client.post('/shorten', 
                            data=json.dumps({'not_url': 'https://example.com'}),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Missing required field: url'
    
    def test_shorten_empty_url(self, client):
        # Test shorten with empty URL
        response = client.post('/shorten', 
                            data=json.dumps({'url': ''}),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'URL cannot be empty'
    
    def test_shorten_invalid_url(self, client):
        # Test shorten with invalid URL format
        response = client.post('/shorten', 
                            data=json.dumps({'url': 'not-a-url'}),
                            content_type='application/json')
        
        assert response.status_code == 422
        data = response.get_json()
        assert 'Invalid URL format' in data['error']
    
    def test_shorten_no_json_body(self, client):
        # Test shorten with no JSON body
        response = client.post('/shorten', 
                            content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Request body must contain valid JSON'
    
    @patch('app.routes.get_short_url')
    def test_shorten_server_error(self, mock_get_short_url, client):
        # Test shorten with server error
        mock_get_short_url.side_effect = Exception("Database error")
        
        response = client.post('/shorten', 
                            data=json.dumps({'url': 'https://example.com'}),
                            content_type='application/json')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Internal server error' in data['error']


class TestRedirectEndpoint(TestRoutes):
    # Test the /<short_url> redirect endpoint

    @patch('app.routes.find_original_url')
    def test_redirect_success(self, mock_find_original_url, client):
        # Test successful redirect
        mock_find_original_url.return_value = "https://example.com"
        
        response = client.get('/abc123')
        
        assert response.status_code == 302
        assert response.location == "https://example.com"
    
    @patch('app.routes.find_original_url')
    def test_redirect_not_found(self, mock_find_original_url, client):
        # Test redirect with non-existent short URL
        mock_find_original_url.return_value = None
        
        response = client.get('/xyz789')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Short URL not found'
        assert data['short_url'] == 'xyz789'
    
    def test_redirect_invalid_format(self, client):
        # Test redirect with invalid short URL format
        response = client.get('/toolongshorturl123')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Invalid short URL format'
    
    @patch('app.routes.find_original_url')
    def test_redirect_server_error(self, mock_find_original_url, client):
        # Test redirect with server error
        mock_find_original_url.side_effect = Exception("Database error")
        
        response = client.get('/abc123')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Internal server error' in data['error']


class TestDecodeEndpoint(TestRoutes):
    # Test the /decode/<short_url> endpoint

    @patch('app.routes.find_original_url')
    def test_decode_success(self, mock_find_original_url, client):
        # Test successful decode
        mock_find_original_url.return_value = "https://example.com"
        
        response = client.get('/decode/abc123')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['original_url'] == 'https://example.com'
        assert data['short_url'] == 'abc123'
    
    @patch('app.routes.find_original_url')
    def test_decode_not_found(self, mock_find_original_url, client):
        # Test decode with non-existent short URL
        mock_find_original_url.return_value = None
        
        response = client.get('/decode/xyz789')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Short URL not found'
        assert data['short_url'] == 'xyz789'
    
    def test_decode_invalid_format(self, client):
        # Test decode with invalid short URL format
        response = client.get('/decode/toolongshorturl123')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Invalid short URL format'
    
    @patch('app.routes.find_original_url')
    def test_decode_server_error(self, mock_find_original_url, client):
        # Test decode with server error
        mock_find_original_url.side_effect = Exception("Database error")
        
        response = client.get('/decode/abc123')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'Internal server error' in data['error']


class TestIntegrationTests(TestRoutes):
    # Integration tests using real database

    @patch('app.models.get_db_connection')
    @patch('app.db.get_db_connection')
    def test_full_workflow_integration(self, mock_db_get_db_connection, mock_models_get_db_connection, client, temp_db):
        # Test complete workflow: shorten -> redirect -> decode
        import sqlite3
        
        # Mock the database connection to use temp database
        def get_temp_connection():
            return sqlite3.connect(temp_db)
        
        mock_db_get_db_connection.side_effect = get_temp_connection
        mock_models_get_db_connection.side_effect = get_temp_connection
        
        # Step 1: Shorten a URL
        response = client.post('/shorten', 
                            data=json.dumps({'url': 'https://example.com'}),
                            content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        short_url = data['short_url']
        
        # Extract the short code from the full URL
        short_code = short_url.split('/')[-1]
        
        # Step 2: Test redirect
        response = client.get(f'/{short_code}')
        assert response.status_code == 302
        assert response.location == 'https://example.com'
        
        # Step 3: Test decode
        response = client.get(f'/decode/{short_code}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['original_url'] == 'https://example.com'
