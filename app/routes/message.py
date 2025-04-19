from flask import jsonify, request
from flask_restx import Namespace, Resource, fields, reqparse
from app.services.case_study import CaseStudyService
from app.services.message import MessageService
from app.utils.system_messages import MISSING_JSON_BODY, REQUIRE_FIELDS



message_ns = Namespace("message", description="message Endpoints")

# Request parsers
message_parser = reqparse.RequestParser()
message_parser.add_argument('title', required=True, type=str)
message_parser.add_argument('decription', required=True, type=str)
message_parser.add_argument('image', required=True, type=str)



@message_ns.route("/create")
class MessageRoutes(Resource):
    def post(self):
        """Create a new message"""
        title = request.form.get("title")
        description = request.form.get("description")
        buttonText = request.form.get("buttonText")
        image = request.files.get("image")  # ✅ from files, not form


        required_fields = {
            "title": title,
            "description": description,
            "buttonText": buttonText,
            "image": image,
        }

        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400

        return MessageService.save(**required_fields)
    
@message_ns.route("/")
class LatestMessageRoutes(Resource):
    def get(self):
        """Get the latest message"""
        latest_message = MessageService.get_latest_message()
        if latest_message:
            return latest_message, 200
        else:
            return {
                "message": "No messages found."
            }, 404

