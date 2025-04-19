from datetime import datetime
from app.extensions import mongo

class Description:

    def __init__(self, **kwargs):  # <-- fixed here
        self.id = kwargs.get("_id")
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.buttonText = kwargs.get("buttonText")
        self.link = kwargs.get("link")
        self.created_at = kwargs.get("created_at")
        self.update_at = kwargs.get("update_at")