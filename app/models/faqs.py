# faq/model.py
from datetime import datetime

from bson import ObjectId
from app.extensions import mongo

class Faq:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.question = kwargs.get('question')
        self.answer = kwargs.get('answer')
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())

    def to_dict(self):
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at_str = self.created_at  # Assume it's already a string

        return {
            "id": str(self.id) if self.id else None,
            "question": self.question,
            "answer": self.answer,
            "created_at": created_at_str,
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
    


    @staticmethod
    def get_faq_by_id(faq_id):
        if not ObjectId.is_valid(faq_id):
            return None
        faq_data = Faq.get_collection().find_one({"_id": ObjectId(faq_id)})
        if faq_data:
            return Faq(**faq_data)
        return None
    
    def update_faq(self,faq_id, data):
        update_data = {}
        if 'question' in data:
            update_data['question'] = data['question']
        if 'answer' in data:
            update_data['answer'] = data['answer']
        update_data['updated_at'] = datetime.utcnow()

        result = self.get_collection().update_one({"_id": ObjectId(faq_id)}, {"$set": update_data})
        return result.modified_count > 0
    

    def delete_faq(self, faq_id):
        result = self.get_collection().delete_one({"_id": ObjectId(faq_id)})
        return result.deleted_count > 0

