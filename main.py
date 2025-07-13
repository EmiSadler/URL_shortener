from flask import Flask
from flask_cors import CORS
import os
from app.db import init_db
from app.routes import register_routes

def create_app():
    """Application factory"""
    app = Flask(__name__, static_folder='/app/static/static', static_url_path='/static')
    
    # Enable CORS for all routes (for frontend development)
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    return app

def main():
    """Initialize database and start the application"""
    init_db()
    app = create_app()
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    main()
