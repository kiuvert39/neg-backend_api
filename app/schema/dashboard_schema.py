from pydantic import BaseModel, Field, validator
from typing import List, Dict


class Testimonial(BaseModel):
    name: str
    position: str
    text: str


class TeamMember(BaseModel):
    name: str
    role: str
    experience: str
    education: str
    file: Dict


class DashboardSchema(BaseModel):
    hero_title: str = Field(..., min_length=1, description="Title of the dashboard")
    hero_highlight: str = Field(..., min_length=1, description="Hero highlight text")
    hero_description: str = Field(..., min_length=1, description="Description for the hero section")
    testimonials: List[Testimonial]
    team_members: List[TeamMember]
    gallery_images: List[str]

    @validator('testimonials')
    def validate_testimonials(cls, v):
        if len(v) == 0:
            raise ValueError('Testimonials cannot be empty')
        return v

    @validator('team_members')
    def validate_team_members(cls, v):
        if len(v) == 0:
            raise ValueError('Team members cannot be empty')
        return v
