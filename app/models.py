from app.shortener import generate_short_url
from app.db import get_db_connection

class Url:
    def __init__(self, id, original_url, short_url):
        self.id = id
        self.original_url = original_url
        self.short_url = short_url

# When a user inputs a long URL, save the long URL to the database,
# generate a short URL, and return the short URL to the user.
# does not check for existing URLs in the database in order to allow the user to create multiple short URLs for the same long URL.
# this would allow the user to track metrics for each short URL separately such as click counts or expiry times
def get_short_url(original_url):
    new_id = save_url_to_db(Url(None, original_url, None))
    short_url = generate_short_url(new_id)
    update_short_url_in_db(new_id, short_url) 
    return short_url

def save_url_to_db(url):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO urls (original_url) VALUES (?)",
            (url.original_url,)  
        )
        url_id = cursor.lastrowid
        conn.commit()
        return url_id

def update_short_url_in_db(url_id, short_url):
    """Update the short_url field for a given URL ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE urls SET short_url = ? WHERE id = ?",
            (short_url, url_id)
        )
        conn.commit()

def find_original_url(short_url):
    """Find the original URL by short_url - needed for redirects"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
        row = cursor.fetchone()
        return row[0] if row else None
