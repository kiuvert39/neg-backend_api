from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.services.auth_service import AuthService
from app.services.blog_service import PostService
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS

post_ns = Namespace("post", description="Blog post Endpoints")

# Request parsers
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', required=True, type=str)
post_parser.add_argument('description', required=True, type=str)
post_parser.add_argument('image', required=True, type=str)
post_parser.add_argument('solution', required=True, type=str)


@post_ns.route("/create")
class Postroutes(Resource):
    # @post_ns.expect(post_parser)
    def post(self):
        """Create a new post"""
        # Get form data instead of JSON
        title = request.form.get("title")
        description = request.form.get("description")
        image_file = request.files.get("image")  # Get the image file
        solution = request.form.get("solution")

        if not title or not description or not image_file or not solution:
            return {"error": REQUIRE_FIELDS }, 400

        return PostService.create(title=title, description=description, image_file=image_file, solution=solution)
    
@post_ns.route("/")
class GetAllPosts(Resource):
    def get(self):
        """Retrieve all posts"""
        return PostService.get_all_posts()


@post_ns.route("/<string:post_id>")
class PostOperations(Resource):

    def get(self, post_id):
        """Retrieve a single post by ID"""
        try:
           
            post = PostService.get_post_by_id(post_id)

            if not post:
             return {"error": "Post not found"}, 404 # Handle 404 here
            
            return post, 200  # No need for jsonify, Flask-RESTX will handle JSON conversion
        except Exception as e:

            return {"error": str(e)}, 500
        

        
    def put(self, post_id):
        """Update an existing post by ID (title, description, solution only)"""
        try:
            update_data = request.json

            # Remove `image` if it exists in the request
            update_data.pop("image", None)

            updated_post = PostService.update_post(post_id, update_data)

            if not updated_post:
                return {"error": "Post not found or not updated"}, 404
            
            return updated_post, 200  
        except Exception as e:
            print("Error in update_post:", str(e))
            return {"error": str(e)}, 500
    
    
# class PostOperations(Resource):
#     def get(self, post_id):
#         """Retrieve a single post by ID"""
#         return PostService.get_post_by_id(post_id)

#     def put(self, post_id):
#         """Update a post"""
#         data = request.form
#         image_file = request.files.get("image")

#         title = data.get("title")
#         description = data.get("description")
#         solution = data.get("solution")

#         if not title and not description and not solution and not image_file:
#             return {"error": "At least one field is required for update"}, 400

#         return PostService.update_post(post_id, title, description, image_file, solution)

#     def delete(self, post_id):
#         """Delete a post"""
#         return PostService.delete_post(post_id)
    

