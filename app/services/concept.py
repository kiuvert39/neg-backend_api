

from datetime import datetime
from app.models.concept import Concepts
from app.services.image_service import ImageService


class ConceptService:

    def create_concept(**kwargs):

        image_file = kwargs.get("image_file")

        url = ImageService.upload_images_to_imgbb([image_file])
        if isinstance(url, dict) and 'error' in url:
            return url
        
        image_file = url

        if not image_file:
            return {"error": "Failed to upload image"}, 500
        
        concept = Concepts(
            heading=kwargs.get("heading"),
            highlight=kwargs.get("highlight"),
            description=kwargs.get("description"),
            highlightDetails=kwargs.get("highlightDetails"),
            image=image_file,
            created_at=datetime.utcnow()
        )
        concept.create_concepts()

        return {
            "message": "Concept created successfully",
        }, 201
    

    def get_concepts():
        concept = Concepts()
        concepts = concept.get_latest_concepts()
        return {
            "concepts": concepts
        }, 200