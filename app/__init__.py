import os
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.config import DevConfig, ProdConfig
from app.extensions import bcrypt, jwt
from app.database import init_db
from app.routes.auth import auth_ns
from app.routes.post import post_ns
from app.routes.homepage import homepage_ns
from app.routes.faq import faq_ns


import logging

def create_app():
    app = Flask(__name__)
 # Choose config based on environment
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)
    # Set up CORS
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"], "supports_credentials": True}})



    # Initialize extensions
    init_db(app)  # Connect to MongoDB
    bcrypt.init_app(app)
    jwt.init_app(app)

 

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Register namespaces
    api = Api(app, title="Flask REST API", version="1.0", description="A simple API", doc="/docs"  )
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(post_ns, path="/post")
    api.add_namespace(homepage_ns, path="/homepage")
    api.add_namespace(faq_ns, path="/faq")

    return app
