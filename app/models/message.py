from datetime import datetime
from app.extensions import mongo


class Message:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.buttonText = kwargs.get('buttonText')
        self.image = kwargs.get('image')
        self.created_at = kwargs.get('created_at')
        self.update_at = kwargs.get('updated_at')


    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at
        
        return {
            "title": self.title,
            "description": self.description,
            "buttonText": self.buttonText,
            "image": self.image,
            "created_at": created_at_str,
        }
    
    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.message
    
    def create_message(self):
        res = self.get_collection().insert_one(self.to_dict())
        return str(res)

