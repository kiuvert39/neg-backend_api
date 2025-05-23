


import requests
from app.config import Config
from app.models.post import Post
from app.services.image_service import ImageService
from app.utils.system_messages import CREATE_POST_SUCCESS, DELETE_POST_SUCCESS, FAILD_TO_UPLOAD_IMAGE, POST_NOT_FOUND, UPDATE_POST_SUCCESS


class PostService:

    def create(**kwargs):
        image_file = kwargs.get("image_file")

        # Upload image (wrap the image in a list since upload_images_to_imgbb expects a list)
        url = ImageService.upload_images_to_imgbb([image_file])  # Pass as a list
        if isinstance(url, dict) and 'error' in url:  # Check if URL contains an error message
            return url  # Return the error response if there is one

        image_url = url  # Assign the URL directly since it returns a string for one image

        if not image_url:
            return {"error": "Failed to upload image"}, 500

        # Create the post using all relevant fields
        post = Post(
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            image=image_url,  # Correctly assign the image URL here
            solution=kwargs.get("solution"),
            subject=kwargs.get("subject")
        )
        post.save()

        return {
            "message": "Post created successfully",
            "post": post.to_dict()
        }, 201



    @staticmethod
    def get_all_posts():
        posts = Post.get_all_posts()
        return {
            "posts": posts
        }, 200
    

    @staticmethod
    def get_post_by_id(post_id):
        """
        Get a post by its ID.
        """
        post = Post.get_post_by_id(post_id)

        if not post:
            return None
        
        if isinstance(post, dict):  # If it's already a dictionary, return it directly
            return post
            
        return post.to_dict()
    


    @staticmethod
    def update_post(post_id, update_data):
        """
        Update a post by its ID (excluding image updates).
        """
        try:
            # First, get the existing post
            post = Post.get_post_by_id(post_id)
            
            if not post:
                print(f"Post with ID {post_id} not found.")
                return None  # Post not found, can't update
            
            # Call update method on the post instance
            success = post.update(update_data)
            
            if not success:
                print(f"Failed to update post with ID {post_id}.")
                return None  # Update failed, return None
            
            # Return the updated post if successful
            return Post.get_post_by_id(post_id)
        
        except Exception as e:
            print("Error in update_post:", str(e))
            return None  # In case of error, return None


    

    # @staticmethod
    # def update_post(post_id, title=None, description=None, image=None, solution=None):
    #     """
    #     Update a post by its ID.
    #     """
    #     post = Post.get_post_by_id(post_id)

    #     if not post:
    #         return {"error": POST_NOT_FOUND }, 404

    #     Post.update_post(post_id, title, description, image, solution)

    #     return {
    #         "message": UPDATE_POST_SUCCESS
    #     }, 200
    
    # @staticmethod
    # def delete_post(post_id):
    #     """
    #     Delete a post by its ID.
    #     """
    #     post = Post.get_post_by_id(post_id)

    #     if not post:
    #         return {"error": POST_NOT_FOUND }, 404

    #     Post.delete_post(post_id)

    #     return {
    #         "message": DELETE_POST_SUCCESS
    #     }, 200
