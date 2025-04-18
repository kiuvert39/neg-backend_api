from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, reqparse
from app.services.description import DescriptionService


description_ns = Namespace("description", description="Description Endpoints")
# Request parsers
description_parser = reqparse.RequestParser()
description_parser.add_argument('title', required=True, type=str)
description_parser.add_argument('decription', required=True, type=str)
description_parser.add_argument('buttonText', required=True, type=str)
description_parser.add_argument('link', required=True, type=str)



@description_ns.route("/create")    
class DescriptionRoutes(Resource):
    def post(self):
        data = request.get_json()

        required_fields = {
            "title": data.get("title"),
            "description": data.get("description"),
            "buttonText": data.get("buttonText"),
            "link": data.get("link"),
            "created_at":datetime.utcnow()
        }

        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400
        
        return DescriptionService.create_description(**required_fields)


@description_ns.route("/")
class DescriptionListRoutes(Resource):
    
    def get(self):

        return DescriptionService.get_description()
