


from app.models.homepage import Homepage
from app.services.image_service import ImageService
from app.utils.system_messages import FAILD_TO_UPLOAD_IMAGE


class HomepageService:

    def create_hero(**kwargs):
        """
        Create a hero section for the homepage.
        """        
        hero = Homepage(
            title=kwargs.get("title"),
            highlight=kwargs.get("highlight"),
            subtitle=kwargs.get("subtitle"),
            description=kwargs.get("description"),
            images=kwargs.get("images") 
        )
        hero.saveHerosection()
        return {
            "message": "Hero section created successfully",
            "hero": hero.to_dict()
        }, 201
    
    
    def get_hero():
        """
        Get the hero section.
        """
        hero = Homepage.get_all_section()
        if not hero:
            return None
        
        return hero

