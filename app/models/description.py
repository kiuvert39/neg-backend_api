from datetime import datetime
from app.extensions import mongo

class Description:

    def __init__(self, **kwargs):  # <-- fixed here
        self.id = kwargs.get("_id")
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.buttonText = kwargs.get("buttonText")
        self.link = kwargs.get("link")
        self.created_at = kwargs.get("created_at")
        self.update_at = kwargs.get("update_at")

    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.description

    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at

        return {
            "title": self.title,
            "description": self.description,
            "buttonText": self.buttonText,
            "link": self.link,
            "created_at": created_at_str,
        }

    def create(self):
        result = self.get_collection().insert_one(self.to_dict())
        return str(result.inserted_id)

    def get_latest_des(self):
        try:
            doc = self.get_collection().find_one(sort=[("created_at", -1)])
            if doc:
                description = Description(**doc).to_dict()
                return description
            else:
                return {"message": "No concepts found."}, 404
        except Exception as e:
            return {"error": str(e)}, 500
