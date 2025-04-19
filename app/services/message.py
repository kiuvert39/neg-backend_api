from datetime import datetime
from app.models.message import Message
from app.services.image_service import ImageService


class MessageService:
    

    @staticmethod
    def save(**kwargs):

        image_file = kwargs.get("image")

        url = ImageService.upload_images_to_imgbb([image_file])
        if isinstance(url, dict) and 'error' in url:
            return url
        
        image_url = url  # Assign the URL directly since it returns a string for one image

        if not image_url:
            return {"error": "Failed to upload image"}, 500

        message = Message(
                        title=kwargs.get("title"),
                        description=kwargs.get("description"),
                        buttonText=kwargs.get("buttonText"),
                        image=image_url,
                        created_at=datetime.utcnow(), 
                    )
        
        message.create_message()

        return {
            "message": "Message created successfully",

        },201
    
    def get_latest_message():
        latest_message = Message.get_collection().find_one({}, sort=[("created_at", -1)])
        if latest_message:
            return Message(**latest_message).to_dict()
        else:
            return None


