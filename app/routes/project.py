from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS
from app.services.project import ProjectService

project_ns = Namespace("case study", description="Case study Endpoints")

# Request parsers
project = reqparse.RequestParser()
project.add_argument('title', required=True, type=str)
project.add_argument('content', required=True, type=str)


@project_ns.route("/create")
class ProjectRoutes(Resource):
    def post(self):
        data = request.get_json()
        required_fields = {
            "title": data.get("title"),
            "content": data.get("content"),
        }
       
        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400
        

        return ProjectService.create_Project(**required_fields)


@project_ns.route("/")
class ProjectListRoutes(Resource):
    """Project List Routes"""
    def get(self):
        """Get all projects"""
        return ProjectService.get_latest_projects()