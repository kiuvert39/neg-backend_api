from app.models.description import Description
class DescriptionService:

    def create_description(**kwargs):

        description = Description(**kwargs)
        description.create()

        return {
            "message": "Description created successfully",
        }, 201
    

    def get_description():
        description = Description()
        descriptions = description.get_latest_des()
        return {
            "descriptions": descriptions
        }, 200
