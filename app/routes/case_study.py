from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.services.case_study import CaseStudyService
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS

caseStudey_ns = Namespace("case study", description="Case study Endpoints")

# Request parsers
caseStudey = reqparse.RequestParser()
caseStudey.add_argument('title', required=True, type=str)
caseStudey.add_argument('content', required=True, type=str)
caseStudey.add_argument('image', required=True, type=str)


@caseStudey_ns.route("/create")
class CaseStudyRoutes(Resource):
    def post(self):
        """Create a new case study"""
        # Get form data instead of JSON
        required_fields = {
            "title": request.form.get("title"),
            "content": request.form.get("content"),
            "image_file": request.files.get("image"),  # Use "image_file" instead of "image"
        }

        # Find missing fields
        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400

        # Pass the fields to the PostService
        return CaseStudyService.create_case_study(**required_fields)


@caseStudey_ns.route("/")
class CaseStudyListRoutes(Resource):
    """Case Study List Routes"""
    def get(self):
        """Get all case studies"""
        return CaseStudyService.get_case_studies()