"""
Pydantic Models for Resume Intelligence Platform.
Defines schemas for candidate extraction, skills, experience, JD analysis, matching, scoring, and recommendation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EducationItem(BaseModel):
    degree: Optional[str] = Field(default=None, description="Degree name, e.g., Bachelor of Technology, M.S.")
    specialization: Optional[str] = Field(default=None, description="Major or field of study, e.g., Computer Science")
    institution: Optional[str] = Field(default=None, description="University or college name")
    graduation_year: Optional[str] = Field(default=None, description="Year of graduation or expected graduation")


class ProjectItem(BaseModel):
    title: str = Field(description="Title or name of the project")
    description: Optional[str] = Field(default=None, description="Summary of project work and responsibilities")
    technologies: List[str] = Field(default_factory=list, description="List of technologies explicitly mentioned in project")
    role: Optional[str] = Field(default=None, description="Role in the project")


class CandidateInfo(BaseModel):
    candidate_name: str = Field(default="Not available", description="Candidate full name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="Location or address")
    education: List[EducationItem] = Field(default_factory=list, description="Education details")
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    job_titles: List[str] = Field(default_factory=list, description="Current or previous job titles")
    companies: List[str] = Field(default_factory=list, description="Companies worked for")
    projects: List[ProjectItem] = Field(default_factory=list, description="Projects listed in resume")
    total_experience: str = Field(default="Not available", description="Total experience mentioned or derived from history")


class SkillsCategorized(BaseModel):
    programming_languages: List[str] = Field(default_factory=list, description="Programming languages explicitly mentioned")
    frameworks: List[str] = Field(default_factory=list, description="Software frameworks mentioned")
    databases: List[str] = Field(default_factory=list, description="Database technologies mentioned")
    cloud_technologies: List[str] = Field(default_factory=list, description="Cloud platforms and services mentioned")
    ai_ml: List[str] = Field(default_factory=list, description="AI/ML libraries and techniques mentioned")
    generative_ai: List[str] = Field(default_factory=list, description="Generative AI, LLM, RAG frameworks mentioned")
    backend_technologies: List[str] = Field(default_factory=list, description="Backend frameworks and tools mentioned")
    frontend_technologies: List[str] = Field(default_factory=list, description="Frontend tools and libraries mentioned")
    devops: List[str] = Field(default_factory=list, description="DevOps, CI/CD, and containerization tools mentioned")
    testing_tools: List[str] = Field(default_factory=list, description="Testing tools and frameworks mentioned")
    other_technical_skills: List[str] = Field(default_factory=list, description="Other technical skills mentioned")


class ExperienceClassification(BaseModel):
    experience_category: str = Field(
        description="Must be one of: 'Fresher', 'Internship experience', 'Entry-level', 'Experienced professional'"
    )
    total_professional_experience: str = Field(default="Not available", description="Total professional work experience duration")
    relevant_experience: str = Field(default="Not available", description="Relevant domain experience duration")
    internship_duration: str = Field(default="Not available", description="Total internship duration if applicable")
    relevant_projects: List[str] = Field(default_factory=list, description="Key relevant projects")
    role_exposure: List[str] = Field(default_factory=list, description="Types of roles or domains exposed to")


class JobDescriptionAnalysis(BaseModel):
    role_title: str = Field(default="Not specified", description="Job title or role name")
    required_skills: List[str] = Field(default_factory=list, description="Mandatory/Required technical and soft skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Good-to-have or preferred skills")
    required_experience: str = Field(default="Not specified", description="Experience requirement specified in JD")
    qualification_requirements: List[str] = Field(default_factory=list, description="Educational or certification requirements")
    role_responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    additional_requirements: List[str] = Field(default_factory=list, description="Other domain or behavioral requirements")


class JobMatchAnalysis(BaseModel):
    matched_skills: List[str] = Field(default_factory=list, description="Skills candidate has that match JD required/preferred skills")
    missing_skills: List[str] = Field(default_factory=list, description="JD skills missing from candidate resume")
    additional_relevant_skills: List[str] = Field(default_factory=list, description="Candidate skills not in JD but relevant")
    relevant_experience_match: str = Field(default="Not evaluated", description="Evaluation of experience vs JD requirement")
    project_alignment: str = Field(default="Not evaluated", description="How candidate projects align with JD responsibilities")
    qualification_alignment: str = Field(default="Not evaluated", description="How education aligns with JD qualifications")
    technology_alignment: str = Field(default="Not evaluated", description="Overall tech stack match assessment")


class CategoryScore(BaseModel):
    category_name: str = Field(description="Name of scoring category (e.g. Skills Match, Relevant Experience)")
    score: float = Field(description="Score out of 100 for this category")
    weight_percent: float = Field(description="Weight percentage allocated to this category")
    weighted_score: float = Field(description="Contribution of this category to overall score")
    justification: str = Field(description="Clear explanation based on resume evidence")


class ExplainableScoring(BaseModel):
    overall_score: float = Field(description="Final overall job match score from 0.0 to 100.0")
    category_scores: List[CategoryScore] = Field(default_factory=list, description="Breakdown of scores by category")
    missing_requirements: List[str] = Field(default_factory=list, description="Key missing candidate requirements")
    scoring_breakdown_summary: str = Field(default="", description="Summary explaining how overall score was computed")


class RecruiterRecommendation(BaseModel):
    recommendation_category: str = Field(
        description="Must be one of: 'Strong Match', 'Potential Match', 'Needs Further Review', 'Low Match'"
    )
    key_strengths: List[str] = Field(default_factory=list, description="Major candidate strengths relative to JD")
    relevant_skills: List[str] = Field(default_factory=list, description="Top relevant skills matching JD")
    relevant_experience_summary: str = Field(default="", description="Summary of relevant experience for recruiter")
    missing_requirements: List[str] = Field(default_factory=list, description="Key gaps or missing requirements")
    areas_requiring_verification: List[str] = Field(default_factory=list, description="Items recruiter should verify in interview")
    overall_jd_alignment_summary: str = Field(default="", description="High-level analytical match recommendation")


class CandidateProfile(BaseModel):
    candidate_id: str = Field(description="Unique candidate identifier like CAND001")
    candidate_name: str = Field(description="Candidate full name")
    resume_filename: str = Field(description="Original resume filename")
    candidate_info: CandidateInfo
    skills: SkillsCategorized
    experience: ExperienceClassification
    job_match: JobMatchAnalysis
    scoring: ExplainableScoring
    recommendation: RecruiterRecommendation
