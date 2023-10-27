from flask import Flask
from psycopg2 import OperationalError
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        test_database_connection()

    from app.view import app as view_app
    app.register_blueprint(view_app)

    jwt = JWTManager(app)

    return app


def test_database_connection():
    try:
        with db.engine.connect():
            print("Database connection successful!")
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")

