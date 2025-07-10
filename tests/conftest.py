"""
Test configuration and utilities for URL shortener tests
"""
import pytest
import tempfile
import os
from unittest.mock import patch


# Test configuration
TEST_DATABASE_NAME = ':memory:'  # Use in-memory database for faster tests


@pytest.fixture
def temp_db_file():
    """Create a temporary database file for tests that need file persistence"""
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    temp_db.close()
    yield temp_db.name
    os.unlink(temp_db.name)


@pytest.fixture
def mock_db_path(temp_db_file):
    """Mock the database path to use temporary file"""
    with patch('app.db.DB_PATH', temp_db_file):
        yield temp_db_file


# Test data fixtures
@pytest.fixture
def valid_urls():
    """Fixture providing valid URLs for testing"""
    return [
        'https://example.com',
        'http://example.com',
        'https://www.example.com',
        'https://subdomain.example.com',
        'https://example.com/path',
        'https://example.com/path?query=1',
        'https://example.com:8080',
        'http://localhost',
        'http://localhost:3000',
        'https://192.168.1.1',
        'https://example.co.uk',
    ]


@pytest.fixture
def invalid_urls():
    """Fixture providing invalid URLs for testing"""
    return [
        None,
        '',
        '   ',
        'example.com',  # Missing protocol
        'ftp://example.com',  # Wrong protocol
        'https://',  # Missing domain
        'not-a-url',
        'javascript:alert("xss")',
        'https://999.999.999.999',  # Invalid IP
        123,  # Not a string
        [],  # Not a string
    ]


@pytest.fixture
def sample_short_urls():
    """Fixture providing sample short URLs for testing"""
    return [
        'e',
        'E',
        '1',
        'emi123',
        'EmI789',
        '2Ly',
        'zZ9',
    ]


@pytest.fixture
def invalid_short_urls():
    """Fixture providing invalid short URLs for testing"""
    return [
        None,
        '',
        '   ',
        'thisURLisTooLong123',  # Too long
        'invalid-chars!',  # Invalid characters
        'spaces here',  # Spaces
    ]


# Test utilities
class TestDataHelper:
    """Helper class for creating test data"""
    
    @staticmethod
    def create_test_url_data(original_url="https://example.com", short_url="abc123"):
        """Create test URL data"""
        return {
            'original_url': original_url,
            'short_url': short_url
        }
    
    @staticmethod
    def create_test_request_data(url="https://example.com"):
        """Create test request data for /shorten endpoint"""
        return {'url': url}
    
    @staticmethod
    def create_invalid_request_data():
        """Create various invalid request data for testing"""
        return [
            None,  # No data
            {},  # Empty object
            {'not_url': 'https://example.com'},  # Wrong field name
            {'url': ''},  # Empty URL
            {'url': None},  # None URL
            {'url': 'invalid-url'},  # Invalid URL
        ]


# Custom assertions for testing
def assert_error_response(response, expected_status, expected_error_message=None):
    """Assert that response is an error with expected status and message"""
    assert response.status_code == expected_status
    assert response.is_json
    
    data = response.get_json()
    assert 'error' in data
    
    if expected_error_message:
        assert expected_error_message in data['error']


def assert_success_response(response, expected_status=200):
    """Assert that response is successful with expected status"""
    assert response.status_code == expected_status
    assert response.is_json


def assert_redirect_response(response, expected_location):
    """Assert that response is a redirect to expected location"""
    assert response.status_code == 302
    assert response.location == expected_location


# Test markers for categorizing tests
pytestmark = pytest.mark.unit  # Mark all tests in this module as unit tests


# Test database setup/teardown
@pytest.fixture(autouse=True)
def reset_database_state():
    """Reset any global database state before each test"""
    # This fixture runs automatically before each test
    yield
    pass
