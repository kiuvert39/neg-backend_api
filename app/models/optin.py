from typing import List, Dict
from app.extensions import mongo

class DashboardModel:
    def __init__(self, hero_title: str, hero_highlight: str, hero_description: str,
                 testimonials: List[Dict], team_members: List[Dict], gallery_images: List[str]):
        self.hero_title = hero_title
        self.hero_highlight = hero_highlight
        self.hero_description = hero_description
        self.testimonials = testimonials
        self.team_members = team_members
        self.gallery_images = gallery_images

    def to_dict(self):
        return {
            "hero_title": self.hero_title,
            "hero_highlight": self.hero_highlight,
            "hero_description": self.hero_description,
            "testimonials": self.testimonials,
            "team_members": self.team_members,
            "gallery_images": self.gallery_images
        }
    
    @staticmethod
    def get_collection():
        if mongo.db is None:
            raise RuntimeError("Database connection is not initialized")
        return mongo.db.optin
    