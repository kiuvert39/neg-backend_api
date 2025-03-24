from flask_pymongo import PyMongo
from flask import Flask
import logging
from pymongo.errors import ConnectionFailure
from app.extensions import mongo


def init_db(app: Flask):
    """
    Initialize the MongoDB connection using the URI from the app config.
    """
    try:
        app.config["MONGO_URI"] = app.config.get("MONGO_URI")  # Ensure it's set
        mongo.init_app(app)

        # Test connection
        mongo.db.command("ping")
        print(f"✅ Connected to MongoDB at {app.config['MONGO_URI']}")
    except ConnectionFailure as e:
        logging.error(f"❌ MongoDB connection failed: {e}")
        raise SystemExit("MongoDB connection failed. Exiting application.")
