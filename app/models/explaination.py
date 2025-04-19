from datetime import datetime
from app.extensions import mongo


class Explaination:

    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.decription1 = kwargs.get('description1')
        self.decription2 = kwargs.get('description2')
        self.buttonText = kwargs.get('buttonText')
        self.buttonLink = kwargs.get('buttonLink')   
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())


    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at
        return {    
            "_id": str(self.id) if self.id else None,
            "title": self.title,
            "description1": self.decription1,
            "description2": self.decription2,
            "buttonText": self.buttonText,
            "buttonLink": self.buttonLink,
            "created_at": created_at_str,
        }
    

    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.explaination