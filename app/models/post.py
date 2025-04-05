from bson import ObjectId
from flask import jsonify
from app.extensions import mongo
from app.utils.system_messages import POST_NOT_FOUND
from datetime import datetime

class Post:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.image = kwargs.get('image')
        self.solution = kwargs.get('solution')
        self.subject = kwargs.get('subject')
        self.created_at = kwargs.get('created_at', datetime.utcnow())  # Set created_at to current time if not provided
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())  # Set updated_at to current time if not provided


    def to_dict(self):
              return {
            "id": str(self.id),  # Convert ObjectId to string
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "solution": self.solution,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else str(self.created_at),
            "updated_at": self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else str(self.updated_at)
        }

 

    @staticmethod
    def get_collection():
        if mongo.db  is None:  # Correct way to check if db is initialized
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.posts  # Get users collection only after MongoDB is ready
    

    def save(self):
        
        post_data = {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "solution": self.solution,
            "subject": self.subject,    
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return self.get_collection().insert_one(post_data)
    

    @classmethod
    def get_all_posts(cls):
        try:
            posts_cursor = cls.get_collection().find()
            posts = [Post(**post).to_dict() for post in posts_cursor]  # Convert cursor to a list
            return posts
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    @classmethod
    def get_post_by_id(cls, post_id):
        """Retrieve a post by its ID."""
        try:
            post = cls.get_collection().find_one({"_id": ObjectId(post_id)})
            if not post:
                return None  

            return cls(**post).to_dict()
        except Exception as e:
            raise Exception(str(e))  # Let the service layer handle the error
        

    def update(self, update_data):
        """Update the post while ensuring `image` remains unchanged."""
        allowed_fields = ["title", "description", "solution"]
        filtered_update_data = {k: v for k, v in update_data.items() if k in allowed_fields}

        if not filtered_update_data:  
            return False
        
         # Ensure the post exists by querying for it
        post = self.get_collection().find_one({"_id": ObjectId(self.id)})
        if not post:
            return False  # Post not found, can't update
            

        print("Datetime now:", datetime.utcnow())  # This should print a valid timestamp

        filtered_update_data["updated_at"] = datetime.utcnow()  # Ensure updated_at is set to current time

            # Log the data being updated
        print(f"Updating post with ID {self.id} with data: {filtered_update_data}")

        # Perform the update operation in the database
        result = self.get_collection().update_one(
            {"_id": self.id},
            {"$set": filtered_update_data}
        )
        
        if result.modified_count > 0:
            print(f"Post with ID {self.id} updated successfully.")
        else:
            print(f"Post with ID {self.id} was not updated (no changes made).")
        
        return result.modified_count > 0  # Return True if at least one document was updated

            
    @classmethod
    def update_post_by_id(cls, post_id, update_data):
        """Find a post by ID and update it."""
        try:
            post = cls.get_post_by_id(post_id)  # Retrieve the existing post
            if not post:
                return None  # Post not found
            
            if isinstance(post, dict):  # Convert dict back to an instance if needed
                post = cls(**post)

            success = post.update(update_data)  # Perform update
            return success
        except Exception as e:
            print("Error in update_post_by_id:", str(e))
            raise Exception(str(e))

    @classmethod
    def delete_post(cls, post_id):
        return cls.get_collection().delete_one({"_id": post_id})
