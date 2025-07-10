import pytest
from app.validators import is_valid_url, validate_shorten_request, validate_short_url, URL_PATTERN


class TestUrlValidation:
    # Test URL validation functions
    
    def test_url_pattern_compilation(self):
        # Test that URL_PATTERN is properly compiled
        assert URL_PATTERN is not None
        assert hasattr(URL_PATTERN, 'match')
        assert hasattr(URL_PATTERN, 'pattern')
    
    def test_is_valid_url_valid_urls(self):
        # Test is_valid_url with valid URLs
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://www.example.com",
            "http://subdomain.example.com",
            "https://example.com/path",
            "https://example.com/path?query=1",
            "https://example.com:8080",
            "http://localhost",
            "http://localhost:3000",
            "https://192.168.1.1",
            "http://192.168.1.1:8080",
            "https://example.co.uk",
        ]
        
        for url in valid_urls:
            assert is_valid_url(url), f"URL should be valid: {url}"
    
    def test_is_valid_url_invalid_urls(self):
        # Test is_valid_url with invalid URLs
        invalid_urls = [
            None,
            "",
            "   ",
            "example.com",  # Missing protocol
            "ftp://example.com",  # Wrong protocol
            "https://",  # Missing domain
            "not-a-url",
            "javascript:alert('xss')",
            "https://999.999.999.999",  # Invalid IP
            123,  # Not a string
            [],  # Not a string
        ]
        
        for url in invalid_urls:
            assert not is_valid_url(url), f"URL should be invalid: {url}"
    
    def test_is_valid_url_edge_cases(self):
        # Test is_valid_url with edge cases
        # Test with whitespace
        assert is_valid_url("  https://example.com  ") == True 
        
        # Test case sensitivity
        assert is_valid_url("HTTPS://EXAMPLE.COM")
        assert is_valid_url("https://EXAMPLE.COM")


class TestShortenRequestValidation:
    # Test validation for /shorten endpoint requests
    
    def test_validate_shorten_request_valid(self):
        # Test valid shorten request
        request_data = {"url": "https://example.com"}
        is_valid, error_response, status_code = validate_shorten_request(request_data, True)
        
        assert is_valid == True
        assert error_response is None
        assert status_code is None
    
    def test_validate_shorten_request_not_json(self):
        # Test request without JSON content type
        request_data = {"url": "https://example.com"}
        is_valid, error_response, status_code = validate_shorten_request(request_data, False)
        
        assert is_valid == False
        assert error_response == {'error': 'Content-Type must be application/json'}
        assert status_code == 400
    
    def test_validate_shorten_request_no_body(self):
        # Test request without JSON body
        is_valid, error_response, status_code = validate_shorten_request(None, True)
        
        assert is_valid == False
        assert error_response == {'error': 'Request body must contain valid JSON'}
        assert status_code == 400
    
    def test_validate_shorten_request_missing_url_field(self):
        # Test request missing 'url' field
        request_data = {"not_url": "https://example.com"}
        is_valid, error_response, status_code = validate_shorten_request(request_data, True)
        
        assert is_valid == False
        assert error_response == {'error': 'Missing required field: url'}
        assert status_code == 400
    
    def test_validate_shorten_request_empty_url(self):
        # Test request with empty URL
        request_data = {"url": ""}
        is_valid, error_response, status_code = validate_shorten_request(request_data, True)
        
        assert is_valid == False
        assert error_response == {'error': 'URL cannot be empty'}
        assert status_code == 400
    
    def test_validate_shorten_request_invalid_url(self):
        # Test request with invalid URL format
        request_data = {"url": "not-a-valid-url"}
        is_valid, error_response, status_code = validate_shorten_request(request_data, True)
        
        assert is_valid == False
        assert error_response == {'error': 'Invalid URL format. URL must start with http:// or https://'}
        assert status_code == 422
    
    def test_validate_shorten_request_url_too_long(self):
        # Test request with URL that's too long
        long_url = "https://example.com/" + "x" * 3000  # Longer than MAX_URL_LENGTH
        request_data = {"url": long_url}
        is_valid, error_response, status_code = validate_shorten_request(request_data, True)
        
        assert is_valid == False
        assert "URL too long" in error_response['error']
        assert status_code == 422


class TestShortUrlValidation:
    # Test validation for short URLs

    def test_validate_short_url_valid(self):
        # Test valid short URL
        is_valid, error_response, status_code = validate_short_url("abc123")
        
        assert is_valid == True
        assert error_response is None
        assert status_code is None
    
    def test_validate_short_url_empty(self):
        # Test empty short URL
        is_valid, error_response, status_code = validate_short_url("")
        
        assert is_valid == False
        assert error_response == {'error': 'Invalid short URL format'}
        assert status_code == 400
    
    def test_validate_short_url_none(self):
        # Test None short URL
        is_valid, error_response, status_code = validate_short_url(None)
        
        assert is_valid == False
        assert error_response == {'error': 'Invalid short URL format'}
        assert status_code == 400
    
    def test_validate_short_url_too_long(self):
        # Test short URL that's too long
        long_short_url = "x" * 20  # Longer than MAX_SHORT_URL_LENGTH
        is_valid, error_response, status_code = validate_short_url(long_short_url)
        
        assert is_valid == False
        assert error_response == {'error': 'Invalid short URL format'}
        assert status_code == 400
    
    def test_validate_short_url_whitespace(self):
        #Test short URL with whitespace
        is_valid, error_response, status_code = validate_short_url("   ")
        
        assert is_valid == False
        assert error_response == {'error': 'Invalid short URL format'}
        assert status_code == 400
