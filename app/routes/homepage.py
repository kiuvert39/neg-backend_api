from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.models.homepage import Homepage
from app.services.auth_service import AuthService
from app.services.blog_service import PostService
from app.services.homepage import HomepageService
from app.services.image_service import ImageService
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS

homepage_ns = Namespace("homepahe", description="Home page Endpoints")

# Request parsers
homep_parser = reqparse.RequestParser()
homep_parser.add_argument('highlight', required=True, type=str)
homep_parser.add_argument('description', required=True, type=str)
homep_parser.add_argument('image', required=True, type=str)
homep_parser.add_argument('created_at', required=True, type=str)
homep_parser.add_argument('updated_at', required=True, type=str)
homep_parser.add_argument('images', required=True, type=str)  # List of image URLs
homep_parser.add_argument('image_file', required=True, type=str)  # Use "image_file" instead of "image"

@homepage_ns.route("/create")
class HomepageRoutes(Resource):
    def post(self):
        """Create a new homepage"""
        # Get form data
        highlight = request.form.get("highlight")
        description = request.form.get("description")
        image_files = request.files.getlist("images")  # List of uploaded image files
        
        # Check for missing fields
        required_fields = {
            "highlight": highlight,
            "description": description,
            "images": image_files  # Ensure we get the list of image files
        }

        # Find missing fields
        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400

        # Upload images using the modified ImageService
        image_urls = ImageService.upload_images_to_imgbb(image_files)
        
        # Handle cases where image upload failed
        if any("error" in url for url in image_urls):
            return {"error": "Image upload failed", "details": image_urls}, 500
        
        # Attach image URLs to required_fields
        required_fields["images"] = image_urls
        
        # Now create the homepage with the provided data
        return HomepageService.create_hero(**required_fields)


@homepage_ns.route("/")
class GetAllHero(Resource):
    def get(self):
        """"""
        return HomepageService.get_hero()