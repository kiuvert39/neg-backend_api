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
from app.routes.case_study import caseStudey_ns
from app.routes.project import project_ns
from app.routes.concept import concept_ns
from app.routes.description import description_ns
from app.routes.optin import dashboard_ns
from app.routes.explaination import explaination_ns
from app.routes.message import message_ns
from app.routes.footer import api as footer_ns




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
    api.add_namespace(caseStudey_ns, path="/case_study")
    api.add_namespace(project_ns, path="/project")
    api.add_namespace(concept_ns, path="/concept")
    api.add_namespace(description_ns, path="/description")
    api.add_namespace(dashboard_ns, path='/dashboard')
    api.add_namespace(explaination_ns, path="/explaination")    
    api.add_namespace(message_ns, path="/message")
    api.add_namespace(footer_ns, path="/footer")





    return app
