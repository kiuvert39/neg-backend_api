from dataclasses import fields
from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from app.services.faq_sservice import FaqService


faq_ns = Namespace("faqs", description="FAQ related operations")


homep_parser = reqparse.RequestParser()

homep_parser.add_argument('question', required=True, type=str)
homep_parser.add_argument('answer', required=True, type=str)
homep_parser.add_argument('created_at', required=True, type=str)
homep_parser.add_argument('updated_at', required=True, type=str)

homep_parser.add_argument('faq_id', required=True, type=str)
homep_parser.add_argument('faq', required=True, type=str)
homep_parser.add_argument('faq_id', required=True, type=str)


@faq_ns.route("/create")
class FaqRoutes(Resource):
    def post(self):
        """Create a new FAQ"""
        # Get form data
        data = request.get_json()

        question = data.get("question")
        answer = data.get("answer")

        # Check for missing fields
        required_fields = {
            "question": question,
            "answer": answer,
        }

        # Find missing fields
        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return {
                "error": "Validation failed",
                "missing_fields": missing_fields,
                "message": "Please provide all required fields."
            }, 400
        
        # Now create the FAQ with the provided data
        faq_service = FaqService()  # Ensure you're instantiating the service correctly
        inserted_id = faq_service.create_faq(question, answer)  # Pass question and answer as arguments

        return {"message": "FAQ created", "faq_id": inserted_id}, 201
    

    
@faq_ns.route("/")
class FaqRoutes(Resource):
    def get(self):
        """Get all FAQs with pagination"""
        page = int(request.args.get('page', 1))  # Default to page 1 if not provided
        per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page

        faq_service = FaqService()
        faqs = faq_service.get_all_faqs(page=page, per_page=per_page)

        if not faqs["faqs"]:
            return {"message": "No FAQs found"}, 404

        return faqs, 200  # Return the pagination data along with FAQs
