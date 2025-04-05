from datetime import datetime
from bson import ObjectId
from flask import jsonify
from flask_pymongo import DESCENDING
from app.extensions import mongo

class Homepage:

    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.highlight = kwargs.get('highlight')
        self.subtitle = kwargs.get('subtitle')
        self.description = kwargs.get('description')
        self.images = kwargs.get('images', [])

        created_at = kwargs.get('created_at')
        updated_at = kwargs.get('updated_at')

        # Convert to datetime if they're strings
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "highlight": self.highlight,
            "subtitle": self.subtitle,
            "description": self.description,
            "images": self.images,  # Assuming you store image URLs here
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else str(self.updated_at)
        }
    
    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.homepage

    def saveHerosection(self):
        hero_data = {
            "title": self.title,
            "highlight": self.highlight,
            "subtitle": self.subtitle,
            "description": self.description,
            "images": self.images,  # Storing image URLs
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return self.get_collection().insert_one(hero_data)

    
    def get_all_section():
        try:
            # Get the latest document based on created_at field
            hero_doc = Homepage.get_collection().find_one(
                sort=[("created_at", DESCENDING)]
            )
            if not hero_doc:
                return {"message": "No hero section found"}, 404
            
            latest_hero = Homepage(**hero_doc)
            return latest_hero.to_dict(), 200

        except Exception as e:
            return {"error": str(e)}, 500
