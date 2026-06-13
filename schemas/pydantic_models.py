from pydantic import BaseModel, Field
from typing import List


class ExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = []


class EducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class ResumeSections(BaseModel):
    skills_section: str = ""
    experience_section: str = ""
    projects_section: str = ""
    education_section: str = ""


class SkillsOutput(BaseModel):
    skills: List[str]


class ExperienceOutput(BaseModel):
    experience: List[ExperienceItem]


class ProjectsOutput(BaseModel):
    projects: List[ProjectItem]


class EducationOutput(BaseModel):
    education: List[EducationItem]


class JDOutput(BaseModel):
    required_skills: List[str]
    optional_skills: List[str]
    experience_required: str
    responsibilities: List[str]


class NormalizedSkills(BaseModel):
    skills: List[str]


class ResumeModel(BaseModel):
    skills: List[str]
    experience: List[ExperienceItem]
    projects: List[ProjectItem]
    education: List[EducationItem]

class ExperienceMatch(BaseModel):
    matched_areas: str
    missing_areas: str
    relevance_score: float = Field(..., description="Score between 0 and 1")

class SuggestionOutput(BaseModel):
    resume_improvements: List[str]
    skill_recommendations: List[str]
    project_suggestions: List[str]
