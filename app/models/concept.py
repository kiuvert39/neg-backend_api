

from datetime import datetime
from bson import ObjectId
from app.extensions import mongo


class Concepts:

    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.heading = kwargs.get('heading')
        self.highlight = kwargs.get('highlight')
        self.description = kwargs.get('description')
        self.highlightDetails = kwargs.get("highlightDetails")
        self.image = kwargs.get('image')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')

    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at

        return {
            "heading": self.heading,
            "highlight": self.highlight,
            "description": self.description,
            "highlightDetails": self.highlightDetails,
            "image": self.image,
            "created_at": created_at_str,
        }
    
    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.concepts
    
    def create_concepts(self):

        concept = self.get_collection().insert_one(self.to_dict())

        return str(concept)
    
    def get_latest_concepts(self):
        try:
            doc = self.get_collection().find_one(sort=[("created_at", -1)])
            if doc:
                concept = Concepts(**doc).to_dict()
                return concept
            else:
                return {"message": "No concepts found."}, 404
        except Exception as e:
            return {"error": str(e)}, 500


