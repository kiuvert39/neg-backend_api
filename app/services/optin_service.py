from app.models.optin import DashboardModel
from app.services.image_service import ImageService
from flask import jsonify
import json
from app.services.image_service import ImageService


class DashboardService:
    @staticmethod
    def create_dashboard(data, team_images, gallery_images):
        try:
            # Upload gallery images to ImgBB
            gallery_image_urls = ImageService.upload_images_to_imgbb(gallery_images)
            if isinstance(gallery_image_urls, dict) and 'error' in gallery_image_urls:
                return gallery_image_urls
            if not gallery_image_urls:
                return {"error": "Failed to upload gallery images"}, 500

            # Upload team images to ImgBB
            team_image_urls = ImageService.upload_images_to_imgbb(team_images)
            if isinstance(team_image_urls, dict) and 'error' in team_image_urls:
                return team_image_urls
            if not team_image_urls:
                return {"error": "Failed to upload team images"}, 500


           # Clean and assign uploaded image URLs to team members
            team_members_raw = data.get("teamMembers", [])
            team_members = []
            for i, member in enumerate(team_members_raw):
                image_url = team_image_urls[i] if i < len(team_image_urls) else None
                
                cleaned_member = {
                    "name": member.get("name", ""),
                    "role": member.get("role", ""),
                    "experience": member.get("experience", ""),
                    "education": member.get("education", ""),
                    "image": image_url
                }
                team_members.append(cleaned_member)


            # Create dashboard model instance
            dashboard = DashboardModel(
                hero_title=data.get("heroTitle", ""),
                hero_highlight=data.get("heroHighlight", ""),
                hero_description=data.get("heroDescription", ""),
                testimonials=data.get("testimonials", []),
                team_members=team_members,
                gallery_images=gallery_image_urls
            )

            # Save to MongoDB
            dashboard_collection = DashboardModel.get_collection()
            inserted = dashboard_collection.insert_one(dashboard.to_dict())

            # Return saved dashboard with MongoDB _id
            saved_dashboard = dashboard.to_dict()
            saved_dashboard["_id"] = str(inserted.inserted_id)
            return saved_dashboard
        except Exception as e:
            print("Error creating dashboard:", e)
            return {"error": "Internal server error"}, 500  



    @staticmethod
    def get_dashboard():
        try:
            dashboard_collection = DashboardModel.get_collection()
            
            # Fetch the most recent dashboard (sorted by _id descending)
            recent_dashboard = dashboard_collection.find_one(sort=[("_id", -1)])
            
            if not recent_dashboard:
                return {"error": "No dashboard found"}, 404

            # Convert ObjectId to string
            recent_dashboard["_id"] = str(recent_dashboard["_id"])

            return recent_dashboard
        except Exception as e:
            print("Error fetching dashboard:", e)
            return {"error": "Internal server error"}, 500