

from datetime import datetime
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