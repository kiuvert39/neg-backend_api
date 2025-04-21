# No SQLAlchemy needed, using MongoDB with pymongo
from app.extensions import mongo

class FooterModel:


    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.footers
    # collection = mongo.db.footers

    @staticmethod
    def create(data):
        return FooterModel.get_collection().insert_one(data)

    @staticmethod
    def get():
        return FooterModel.get_collection().find_one(sort=[('_id', -1)], projection={'_id': False})

    @staticmethod
    def update(data):
        return FooterModel.get_collection().update_one({}, {"$set": data}, upsert=True)
