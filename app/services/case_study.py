
from datetime import datetime
from app.models.casestudy import CaseStudy
from app.services.image_service import ImageService


class CaseStudyService:

    def create_case_study(**kwargs):
        # Logic to create a case study
        
        image_file = kwargs.get("image_file")

        url = ImageService.upload_images_to_imgbb([image_file])
        if isinstance(url, dict) and 'error' in url:
            return url
        
        image_url = url  # Assign the URL directly since it returns a string for one image

        if not image_url:
            return {"error": "Failed to upload image"}, 500
        
        case_study = CaseStudy(
            title=kwargs.get("title"),
            content=kwargs.get("content"),
            image=image_url,
            created_at=datetime.utcnow()
        )

        case_study.create_case_study()

        return {
            "message": "Case study created successfully",
        }, 201


    def get_case_studies():
        case_study = CaseStudy()
        case_studies = case_study.get_latest_case_studies()
        return {
            "case_studies": case_studies
        }, 200