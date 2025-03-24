from app.extensions import mongo


class User:

    @staticmethod
    def get_collection():
        if mongo.db  is None:  # Correct way to check if db is initialized
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.users  # Get users collection only after MongoDB is ready


    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = password
    

    def save(self):
        
        user_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return self.get_collection().insert_one(user_data)  
    
    @classmethod
    def find_by_email(cls, email):
        return cls.get_collection().find_one({"email": email})