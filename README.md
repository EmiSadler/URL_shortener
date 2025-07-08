# URL Shortener

A Python backend service for shortening URLs using Flask and SQLite.

## Setup & Testing

1. **Run the application:**

   ```bash
   python main.py
   ```

   Server will start on `http://localhost:8000`

2. **Test the API:**

   **Health Check:**

   ```bash
   curl http://localhost:8000/
   ```

   **Create a short URL:**

   ```bash
   curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}' \
     http://localhost:8000/shorten
   ```

   **Test redirect (use the short_url from previous response):**

   ```bash
   curl -L http://localhost:8000/1
   ```

   **Decode a short URL:**

   ```bash
   curl http://localhost:8000/decode/1
   ```
