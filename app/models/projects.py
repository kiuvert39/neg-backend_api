from app.extensions import mongo


from datetime import datetime


class Project:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())


    
    @staticmethod
    def get_collection():
        if mongo.db  is None:  # Correct way to check if db is initialized
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.project 
    

    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at  # Assume it's already a string

        return {
            "id": str(self.id) if self.id else None,
            "title": self.title,
            "content": self.content,
            "created_at": created_at_str,
        }
    

    def create_project(self):
        # Insert project into the collection
        result = self.get_collection().insert_one(self.to_dict())
        return str(result)



    def get_latest_case_studies(self, limit=5):
        try:
            projects = self.get_collection().find().sort("created_at", -1).limit(limit)
            project = [Project(**case_study).to_dict() for case_study in projects]
            return project
        except Exception as e:
            return {"error": str(e)},
