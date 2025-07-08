from flask import Flask
from app.db import init_db
from app.routes import register_routes

app = Flask(__name__)

def main():
    init_db()                    # Setup database
    register_routes(app)         # Connect routes to app
    app.run(debug=True)          # Start the server

if __name__ == "__main__":
    main()

