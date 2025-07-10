import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from app.models import Url, get_short_url, save_url_to_db, update_short_url_in_db, find_original_url
from app.db import get_db_connection, init_db


class TestUrlModel:
    # Test the Url class

    def test_url_initialization(self):
        # Test that Url class initializes correctly
        url = Url(1, "https://example.com", "abc123")
        
        assert url.id == 1
        assert url.original_url == "https://example.com"
        assert url.short_url == "abc123"
    
    def test_url_initialization_with_none_values(self):
        # Test Url class with None values
        url = Url(None, "https://example.com", None)
        
        assert url.id is None
        assert url.original_url == "https://example.com"
        assert url.short_url is None


class TestDatabaseOperations:
    # Test database operations

    @pytest.fixture
    def temp_db(self):
        # Create a temporary database and file for testing
        temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        temp_db_file.close()
        
        # Mock the database path
        with patch('app.db.DB_PATH', temp_db_file.name):
            init_db()  # Initialize the test database
            yield temp_db_file.name
        
        # Clean up
        os.unlink(temp_db_file.name)
    
    def test_save_url_to_db(self, temp_db):
        # Test saving a URL to the database
        url = Url(None, "https://example.com", None)
        
        with patch('app.db.DB_PATH', temp_db):
            url_id = save_url_to_db(url)
            
            assert url_id is not None
            assert isinstance(url_id, int)
            assert url_id >= 10000  # Should start from 10000
    
    def test_update_short_url_in_db(self, temp_db):
        # Test updating short URL in database
        url = Url(None, "https://example.com", None)
        
        with patch('app.db.DB_PATH', temp_db):
            # First save the URL
            url_id = save_url_to_db(url)
            
            # Then update the short URL
            update_short_url_in_db(url_id, "abc123")
            
            # Verify it was updated
            original_url = find_original_url("abc123")
            assert original_url == "https://example.com"
    
    def test_find_original_url(self, temp_db):
        # Test finding original URL by short URL
        url = Url(None, "https://example.com", None)
        
        with patch('app.db.DB_PATH', temp_db):
            url_id = save_url_to_db(url)
            update_short_url_in_db(url_id, "abc123")
            
            # Test finding existing URL
            original_url = find_original_url("abc123")
            assert original_url == "https://example.com"
            
            # Test finding non-existent URL
            original_url = find_original_url("nonexistent")
            assert original_url is None


class TestGetShortUrl:
    # Test the main get_short_url function

    @patch('app.models.save_url_to_db')
    @patch('app.models.generate_short_url')
    @patch('app.models.update_short_url_in_db')
    def test_get_short_url_success(self, mock_update, mock_generate, mock_save):
        # Test successful short URL generation
        # Setup mocks
        mock_save.return_value = 10000
        mock_generate.return_value = "abc123"
        
        # Test the function
        result = get_short_url("https://example.com")
        
        # Verify the result
        assert result == "abc123"
        
        # Verify the function calls
        mock_save.assert_called_once()
        mock_generate.assert_called_once_with(10000)
        mock_update.assert_called_once_with(10000, "abc123")
    
    @patch('app.models.save_url_to_db')
    def test_get_short_url_database_error(self, mock_save):
        # Test handling database errors
        # Setup mock to raise an exception
        mock_save.side_effect = Exception("Database error")
        
        # Test that the exception is propagated
        with pytest.raises(Exception, match="Database error"):
            get_short_url("https://example.com")
