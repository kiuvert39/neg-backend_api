

from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest
from bson import ObjectId
from app.models.faqs import Faq


class FaqService:

    @staticmethod
    def create_faq(question, answer):
        
        faq = Faq(
            question=question,
            answer=answer,
            created_at=datetime.utcnow()
        )
        
        # Call the create_faq method from Faq model to insert it into the database
        inserted_id = faq.create_faq()  # Notice that we're not passing the entire faq object here

        return inserted_id
    
    def get_all_faqs(self, page=1, per_page=10):
        # Calculate the number of documents to skip
        skip = (page - 1) * per_page

        # Retrieve the paginated results
        faqs = Faq.get_collection().find().skip(skip).limit(per_page)

        # Convert the FAQ objects to dictionaries
        faq_list = [Faq(**faq).to_dict() for faq in faqs]

        # Get the total count of FAQs for pagination metadata
        total_faqs = Faq.get_collection().count_documents({})

        return {
            "faqs": faq_list,
            "total_faqs": total_faqs,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_faqs + per_page - 1) // per_page  # Round up to get the total pages
        }
    
    @staticmethod
    def get_faq_by_id(faq_id):
        if not ObjectId.is_valid(faq_id):
            raise BadRequest('Invalid FAQ ID format')

        faq = Faq().get_faq_by_id(faq_id)
        if not faq:
            raise NotFound('FAQ not found')

        return faq.to_dict()

    def update_faq(faq_id, data):
        if not ObjectId.is_valid(faq_id):
            raise BadRequest('Invalid FAQ ID format')
        
        faq = Faq()

        updated = faq.update_faq(faq_id, data)
        if not updated:
            raise NotFound('FAQ not found or no change made')
        return {'message': 'FAQ updated successfully'}
    
    def delete_faq(faq_id):
        if not ObjectId.is_valid(faq_id):
            raise BadRequest('Invalid FAQ ID format')
        faq = Faq()
        deleted = faq.delete_faq(faq_id)
        if not deleted:
            raise NotFound('FAQ not found')
        return {'message': 'FAQ deleted successfully'}