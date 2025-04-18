from app.models.projects import Project
from datetime import datetime

class ProjectService:


    def create_Project(**kwargs):


        project = Project(
            title=kwargs.get("title"),
            content=kwargs.get("content"),
            created_at=datetime.utcnow()
        )

        project = project.create_project()
        return {
            "message": "Project created successfully",
        }, 201
    
    def get_latest_projects():
        project = Project()
        projects = project.get_latest_case_studies()
        return {
            "projects": projects
        }, 200