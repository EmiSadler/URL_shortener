from flask import Flask
from flask_cors import CORS
from app.db import init_db
from app.routes import register_routes

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Enable CORS for all routes (for frontend development)
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    return app

def main():
    """Initialize database and start the application"""
    init_db()
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == "__main__":
    main()
