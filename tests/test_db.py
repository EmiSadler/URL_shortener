import pytest
import tempfile
import os
from unittest.mock import patch
from app.db import get_db_connection, init_db, DB_PATH


class TestDatabaseConnection:
    
    @pytest.fixture
    def temp_db(self):
        temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        temp_db_file.close()
        yield temp_db_file.name
        os.unlink(temp_db_file.name)
    
    def test_get_db_connection(self, temp_db):
        # Test database connection creation
        with patch('app.db.DB_PATH', temp_db):
            conn = get_db_connection()
            
            assert conn is not None
            assert hasattr(conn, 'cursor')
            assert hasattr(conn, 'execute')
            assert hasattr(conn, 'commit')
            assert hasattr(conn, 'close')
            
            # Test executing a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
            
            conn.close()
    
    def test_get_db_connection_context_manager(self, temp_db):
        # Test database connection as context manager
        with patch('app.db.DB_PATH', temp_db):
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1
            
            # Connection should be closed after context manager
            # SQLite doesn't have a direct way to check if closed, but we can test
            # that the connection object still exists
            assert conn is not None


class TestDatabaseInitialization:
    # Test database initialization functions
    
    @pytest.fixture
    def temp_db(self):
        # Create a temporary database file
        temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        temp_db_file.close()
        yield temp_db_file.name
        os.unlink(temp_db_file.name)
    
    def test_init_db_creates_table(self, temp_db):
        # Test that init_db creates the urls table
        with patch('app.db.DB_PATH', temp_db):
            init_db()
            
            # Check that the table exists
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
                result = cursor.fetchone()
                assert result is not None
                assert result[0] == 'urls'
    
    def test_init_db_creates_correct_schema(self, temp_db):
        # Test that init_db creates the correct table schema
        with patch('app.db.DB_PATH', temp_db):
            init_db()
            
            # Check the table schema
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(urls)")
                columns = cursor.fetchall()
                
                # Should have 4 columns: id, original_url, short_url, created_at
                assert len(columns) == 4
                
                # Check column details
                column_names = [col[1] for col in columns]
                assert 'id' in column_names
                assert 'original_url' in column_names
                assert 'short_url' in column_names
                assert 'created_at' in column_names
                
                # Check that id is primary key and autoincrement
                id_column = next(col for col in columns if col[1] == 'id')
                assert id_column[5] == 1  # Primary key flag
    
    def test_init_db_sets_starting_id(self, temp_db):
        # Test that init_db sets the starting ID to 10000
        with patch('app.db.DB_PATH', temp_db):
            init_db()
            
            # Check that sqlite_sequence is set for starting ID
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='urls'")
                result = cursor.fetchone()
                assert result is not None
                assert result[0] == 9999  # Should be set to 9999 so next ID is 10000
    
    def test_init_db_idempotent(self, temp_db):
        # Test that init_db can be called multiple times safely
        with patch('app.db.DB_PATH', temp_db):
            # Call init_db multiple times
            init_db()
            init_db()
            init_db()
            
            # Should still work and have correct schema
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
                result = cursor.fetchone()
                assert result is not None
                assert result[0] == 'urls'
    
    def test_init_db_doesnt_reset_sequence_if_data_exists(self, temp_db):
        # Test that init_db doesn't reset sequence if data already exists
        with patch('app.db.DB_PATH', temp_db):
            # Initialize database
            init_db()
            
            # Insert some data
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", 
                            ('https://example.com', 'abc123'))
                conn.commit()
            
            # Call init_db again
            init_db()
            
            # Check that data still exists
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM urls")
                count = cursor.fetchone()[0]
                assert count == 1
                
                # Check that the sequence wasn't reset
                cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='urls'")
                result = cursor.fetchone()
                # Should be greater than 9999 since we inserted data
                assert result[0] >= 10000


class TestDatabasePath:
    # Test database path configuration

    def test_db_path_exists(self):
        # Test that DB_PATH is properly configured
        assert DB_PATH is not None
        assert str(DB_PATH) == 'url_shortener.db'
    
    def test_db_path_is_pathlib_path(self):
        # Test that DB_PATH is a pathlib Path object
        from pathlib import Path
        assert isinstance(DB_PATH, Path)
