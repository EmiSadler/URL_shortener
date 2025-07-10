import pytest
from app.shortener import generate_short_url


class TestGenerateShortUrl:
# Test cases for the generate_short_url function
    
    def test_generate_short_url_basic(self):
        # Test basic short URL generation
        # Test with known values
        assert generate_short_url(0) == "0"
        assert generate_short_url(1) == "1"
        assert generate_short_url(61) == "Z"
        assert generate_short_url(62) == "10"
    
    def test_generate_short_url_starting_id(self):
        # Test short URL generation starting from 10000
        short_url = generate_short_url(10000)
        assert short_url is not None
        assert len(short_url) >= 1
        assert isinstance(short_url, str)
    
    def test_generate_short_url_sequential(self):
        # Test that sequential IDs generate different short URLs
        url1 = generate_short_url(10000)
        url2 = generate_short_url(10001)
        url3 = generate_short_url(10002)
        
        # Should all be different
        assert url1 != url2
        assert url2 != url3
        assert url1 != url3
        
        # Should all be strings
        assert isinstance(url1, str)
        assert isinstance(url2, str)
        assert isinstance(url3, str)
    
    def test_generate_short_url_character_set(self):
        # Test that generated URLs only contain valid base62 characters
        valid_chars = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        # Test with various IDs
        test_ids = [0, 1, 61, 62, 123, 1000, 10000, 50000, 100000]
        
        for test_id in test_ids:
            short_url = generate_short_url(test_id)
            url_chars = set(short_url)
            
            # All characters should be in the valid set
            assert url_chars.issubset(valid_chars), f"Invalid characters in URL for ID {test_id}: {short_url}"
    
    def test_generate_short_url_length_growth(self):
        # Test that URL length grows appropriately with larger IDs
        # Smaller IDs should generally produce shorter URLs
        small_url = generate_short_url(10)
        medium_url = generate_short_url(10000)
        large_url = generate_short_url(1000000)
        
        # Check that lengths are reasonable
        assert len(small_url) >= 1
        assert len(medium_url) >= 1
        assert len(large_url) >= 1
        
        # Larger IDs should generally produce longer URLs (though not always strictly)
        assert len(large_url) >= len(small_url)
    
    def test_generate_short_url_edge_cases(self):
        # Test edge cases for short URL generation
        # Test with very large number
        large_url = generate_short_url(999999999)
        assert large_url is not None
        assert len(large_url) > 0
        
        # Test with maximum reasonable ID
        max_url = generate_short_url(62**10)  # Very large base62 number
        assert max_url is not None
        assert len(max_url) > 0
    
    def test_generate_short_url_consistency(self):
        # Test that same ID always generates same URL
        test_id = 12345
        
        # Generate the same URL multiple times
        url1 = generate_short_url(test_id)
        url2 = generate_short_url(test_id)
        url3 = generate_short_url(test_id)
        
        # Should all be identical
        assert url1 == url2 == url3
    
