# faq/model.py
from datetime import datetime

from bson import ObjectId
from app.extensions import mongo

class Faq:
    def __init__(self, **kwargs):
        self.id = kwargs.get("_id")
        self.question = kwargs.get("question")
        self.answer = kwargs.get("answer")
        self.created_at = kwargs.get("created_at")

    def to_dict(self):
        # Convert datetime fields to string
        return {
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
        }

    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.faqs
    
    def create_faq(self):
        # Insert faq into the collection
        result = self.get_collection().insert_one(self.to_dict())
        return str(result.inserted_id)  # Return the inserted id
