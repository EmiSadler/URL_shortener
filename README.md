# URL Shortener

A Python backend service for shortening URLs using Flask and SQLite.

## Features

- ✅ Create short URLs from long URLs
- ✅ Redirect short URLs to original URLs
- ✅ Decode short URLs to see original without redirecting
- ✅ Multiple short URLs allowed for same long URL (for tracking)
- ✅ Base62 encoding for short, readable URLs
- ✅ SQLite database for persistence
- ✅ IDs start at 10000 for better-looking short URLs

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   python main.py
   ```

   You should see:

   ```
   Starting URL Shortener on http://localhost:8000
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:8000
   ```

## API Testing

### 1. Health Check

Test if the server is running:

```bash
curl http://localhost:8000/
```

**Expected Response:**

```json
{ "message": "URL Shortener API is running!" }
```

### 2. Create Short URL

Convert a long URL to a short one:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}' \
  http://localhost:8000/shorten
```

**Expected Response:**

```json
{ "short_url": "2Bi" }
```

_Note: Your actual short URL will vary but will be 3+ characters_

### 3. Test Redirect

Use the short URL to redirect to the original:

```bash
curl -L http://localhost:8000/2Bi
```

This will redirect you to https://www.google.com (showing in the CLI the HTML content from Google's homepage)

alternatively:

```bash
curl -I http://localhost:8000/2Bi
```

This will show you the redirect response instead of following it (cleaner in the CLI)

### 4. Decode Short URL

Get the original URL without redirecting:

```bash
curl http://localhost:8000/decode/2Bi
```

**Expected Response:**

```json
{ "original_url": "https://www.google.com" }
```

### 5. Test Multiple URLs

Create several short URLs:

```bash
# GitHub
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/EmiSadler"}' \
  http://localhost:8000/shorten

# Bootcamp Simulator
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://bootcampsim.netlify.app/"}' \
  http://localhost:8000/shorten
```

### 6. Error Handling

Test with missing URL:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  http://localhost:8000/shorten
```

Test with non-existent short URL:

```bash
curl http://localhost:8000/xyz123
```

## API Endpoints

| Method | Endpoint              | Description                       |
| ------ | --------------------- | --------------------------------- |
| `GET`  | `/`                   | Health check                      |
| `POST` | `/shorten`            | Create short URL from long URL    |
| `GET`  | `/<short_url>`        | Redirect to original URL          |
| `GET`  | `/decode/<short_url>` | Get original URL without redirect |

## Project Structure

```
URL_shortener/
├── app/
│   ├── __init__.py
│   ├── db.py           # Database connection and initialization
│   ├── models.py       # URL model and database operations
│   ├── routes.py       # Flask API routes
│   ├── shortener.py    # Short URL generation logic (base62)
│   └── utils.py        # Utility functions
├── tests/              # Test files
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
├── url_shortener.db   # SQLite database (created automatically)
└── README.md
```

## How It Works

1. **URL Submission**: User submits a long URL via POST request
2. **ID Generation**: Database assigns an ID starting from 10000
3. **Short Code Creation**: ID is converted to base62 (0-9, a-z, A-Z)
4. **Database Storage**: Both original URL and short code are saved
5. **Response**: Short code is returned to user

## Technical Details

- **Database**: SQLite with auto-incrementing IDs starting at 10000
- **Encoding**: Base62 encoding for compact, readable URLs
- **Port**: Runs on port 8000
- **Framework**: Flask
- **URL Format**: `http://localhost:8000/<short_code>`

## Troubleshooting

**Port 8000 in use?**

- Kill the process: `lsof -ti:8000 | xargs kill -9`
- Or change the port in `main.py`

**Database issues?**

- Delete and recreate: `rm url_shortener.db` then restart the app
