from app.db import init_db
from app.routes import app as routes_app
from flask import Flask

def main():
    init_db()

if __name__ == "__main__":
    main()

app = Flask(__name__)
