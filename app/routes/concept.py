from flask import request
from flask_restx import Namespace, Resource, reqparse

from app.services.concept import ConceptService


concept_ns = Namespace("concept", description="Concept Endpoints")
# Request parsers

concept_parser = reqparse.RequestParser()
concept_parser.add_argument('heading', required=True, type=str)
concept_parser.add_argument('highlight', required=True, type=str)
concept_parser.add_argument('description', required=True, type=str)
concept_parser.add_argument('highlightDetails', required=True, type=str)
concept_parser.add_argument('image_file', required=True, type=str)


@concept_ns.route("/create")
class ConceptRoutes(Resource):
    def post(self):

        required_fields = {
            "heading": request.form.get("heading"),
            "highlight": request.form.get("highlight"),
            "description": request.form.get("description"),
            "highlightDetails": request.form.get("highlightDetails"),
            "image_file": request.files.get("image"),
        }

        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400
        
        return ConceptService.create_concept(**required_fields)
    
@concept_ns.route("/")
class ConceptListRoutes(Resource):
    
    def get(self):

        return ConceptService.get_concepts()