from datetime import datetime

from bson import ObjectId

from app.models.explaination import Explaination


class ExplainationService:

    @staticmethod
    def create_explaination(data):
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = Explaination.get_collection().insert_one(data)
        new_explaination = Explaination.get_collection().find_one({"_id": result.inserted_id})
        return Explaination(**new_explaination)
    
    @staticmethod
    def get_latest_explaination():
        doc = Explaination.get_collection().find_one(sort=[('created_at', -1)])
        if doc:
            return Explaination(**doc)
        return None
    
    @staticmethod
    def update_explaination(explaination_id, data):
        data['updated_at'] = datetime.utcnow()
        result = Explaination.get_collection().update_one(
            {"_id": ObjectId(explaination_id)},
            {"$set": data}
        )
        if result.modified_count > 0:
            updated = Explaination.get_collection().find_one({"_id": ObjectId(explaination_id)})
            return Explaination(**updated)
        return None
