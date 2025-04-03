


import requests
from app.config import Config
from app.models.post import Post
from app.services.image_service import ImageService
from app.utils.system_messages import CREATE_POST_SUCCESS, DELETE_POST_SUCCESS, FAILD_TO_UPLOAD_IMAGE, POST_NOT_FOUND, UPDATE_POST_SUCCESS


class PostService:

    def create(title, description, image_file, solution):

        url = ImageService.upload_image_to_imgbb(image_file=image_file)
        if 'error' in url:
            return url # Return the error response if there is one
        
        
        image_url = url
        
        # If no display_url was found, return an error
        if not image_url:
            return {"error": FAILD_TO_UPLOAD_IMAGE}, 500


        post = Post(title=title, description=description, image=image_url, solution=solution)
        post.save()
        return {
            "message": CREATE_POST_SUCCESS,
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
