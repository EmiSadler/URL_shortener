# URL Shortener

A full-stack URL shortener application with a Python Flask backend and React frontend.

🚀 **Live Demo**: [https://url-shortener.sadlers.cloud/](https://url-shortener.sadlers.cloud/)

## Features

### Backend (Flask + SQLite)

- ✅ Create short URLs from long URLs
- ✅ Redirect short URLs to original URLs
- ✅ Multiple short URLs allowed for same long URL (for tracking)
- ✅ Base62 encoding for short, readable URLs
- ✅ SQLite database for persistence
- ✅ IDs start at 10000 for better-looking short URLs
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling and validation

### Frontend (React)

- ✅ Modern, responsive UI with gradient background
- ✅ Real-time URL validation
- ✅ Copy shortened URL to clipboard
- ✅ Test shortened URLs directly in the interface
- ✅ Loading states and error handling
- ✅ Success notifications

## Quick Start

### Option 1: Use the Development Startup Script (Recommended)

```bash
./start-dev.sh
```

This will start both the backend (port 8000) and frontend (port 3000) automatically.

### Option 2: Manual Setup

#### Backend Setup

1. **Set up Virtual Environment**

   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend:**

   ```bash
   python main.py
   ```

#### Frontend Setup

1. **Install Node.js dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the React development server:**

   ```bash
   npm start
   ```

## Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

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

### 4. Test Multiple URLs

Create several short URLs:

```bash
# GitHub
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/EmiSadler/URL_shortener"}' \
  http://localhost:8000/shorten

# Bootcamp Simulator
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"url": "https://bootcampsim.netlify.app/"}' \
  http://localhost:8000/shorten
```

### 5. Error Handling

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

## Production Build

### Build Frontend for Production

```bash
./build-prod.sh
```

Or manually:

```bash
cd frontend
npm run build
```

### Serve Production Build

Option 1 - Using a static file server:

```bash
npm install -g serve
serve -s frontend/build -l 3000
```

Option 2 - Using Python's built-in server:

```bash
cd frontend/build
python -m http.server 3000
```

### Production Deployment

For production deployment:

1. **Backend**: Use a WSGI server like Gunicorn

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:create_app()
   ```

2. **Frontend**: Serve the built files using a web server like Nginx or Apache

3. **Database**: Consider using PostgreSQL for production instead of SQLite

## API Endpoints

| Method | Endpoint       | Description                    |
| ------ | -------------- | ------------------------------ |
| `GET`  | `/`            | Health check                   |
| `POST` | `/shorten`     | Create short URL from long URL |
| `GET`  | `/<short_url>` | Redirect to original URL       |

## Project Structure

```
URL_shortener/
├── app/                    # Backend Flask application
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── db.py              # Database connection and initialization
│   ├── models.py          # URL model and database operations
│   ├── routes.py          # Flask API routes
│   ├── shortener.py       # Short URL generation logic (base62)
│   ├── validators.py      # Input validation functions
│   └── error_handlers.py  # Error handling utilities
├── frontend/               # React frontend application
│   ├── public/
│   │   ├── index.html     # HTML template
│   │   └── manifest.json  # PWA manifest
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Header.js      # App header
│   │   │   ├── Footer.js      # App footer
│   │   │   └── URLShortener.js # Main URL shortener form
│   │   ├── App.js         # Main App component
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # Node.js dependencies
│   └── build/             # Production build (after npm run build)
├── tests/                  # Test files for backend
├── .github/                # GitHub Actions CI/CD
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── main.py                # Backend entry point
├── requirements.txt       # Python dependencies
├── start-dev.sh           # Development startup script
├── build-prod.sh          # Production build script
├── url_shortener.db       # SQLite database (created automatically)
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
