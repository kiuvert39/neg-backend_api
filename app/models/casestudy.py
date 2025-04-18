from datetime import datetime

from bson import ObjectId
from app.extensions import mongo

class CaseStudy:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.image = kwargs.get('image')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at  # Assume it's already a string

        return {
            "id": str(self.id) if self.id else None,
            "title": self.title,
            "content": self.content,
            "image": self.image,
            "created_at": created_at_str,
        }


    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.casestudies
    
    def create_case_study(self):
        # Insert case study into the collection
        result = self.get_collection().insert_one(self.to_dict())
        return str(result)


    def get_latest_case_studies(self, limit=4):
        try:
            case_studies_cursor = self.get_collection().find().sort("created_at", -1).limit(limit)
            case_studies = [CaseStudy(**case_study).to_dict() for case_study in case_studies_cursor]
            return case_studies
        except Exception as e:
            return {"error": str(e)}, 500
