from flask import Flask
from flask_restx import Api
from app.config import DevConfig
from app.extensions import bcrypt, jwt
from app.database import init_db
from app.routes.auth import auth_ns
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)  # Load config

    # Initialize extensions
    init_db(app)  # Connect to MongoDB
    bcrypt.init_app(app)
    jwt.init_app(app)

 

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Register namespaces
    api = Api(app, title="Flask REST API", version="1.0", description="A simple API")
    api.add_namespace(auth_ns, path="/auth")

    return app
