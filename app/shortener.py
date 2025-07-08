# Short URL generator using base62 encoding - takes in id from db
def generate_short_url(url_id):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    short_url = []

    while url_id > 0:
        url_id, remainder = divmod(url_id, base)
        short_url.append(characters[remainder])

    return ''.join(reversed(short_url)) if short_url else characters[0]

# divmod - returns a tuple of the quotient and remainder when dividing two numbers (x//y, x%y)
