from typing import List

"""Pydantic schemas used to validate extracted resume and JD data."""

from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: str = ""


class ProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)


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
    skills: List[str] = Field(default_factory=list)


class ExperienceOutput(BaseModel):
    experience: List[ExperienceItem] = Field(default_factory=list)


class ProjectsOutput(BaseModel):
    projects: List[ProjectItem] = Field(default_factory=list)


class EducationOutput(BaseModel):
    education: List[EducationItem] = Field(default_factory=list)


class JDOutput(BaseModel):
    required_skills: List[str] = Field(default_factory=list)
    optional_skills: List[str] = Field(default_factory=list)
    experience_required: str = ""
    responsibilities: List[str] = Field(default_factory=list)


class NormalizedSkills(BaseModel):
    skills: List[str] = Field(default_factory=list)


class ResumeModel(BaseModel):
    skills: List[str] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)


class ExperienceMatch(BaseModel):
    matched_areas: List[str] = Field(default_factory=list)
    missing_areas: List[str] = Field(default_factory=list)
    relevance_score: float = Field(
        default=0,
        ge=0,
        le=1,
        description="Score between 0 and 1",
    )


class SuggestionOutput(BaseModel):
    resume_improvements: List[str] = Field(default_factory=list)
    skill_recommendations: List[str] = Field(default_factory=list)
    project_suggestions: List[str] = Field(default_factory=list)
