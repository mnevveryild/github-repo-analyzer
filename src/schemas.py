from typing import List, Literal
from pydantic import BaseModel


class TechStack(BaseModel):
    languages: List[str]
    frameworks: List[str]
    databases: List[str] = []
    tools: List[str] = []
    cloud_services: List[str] = []


class Suggestion(BaseModel):
    category: Literal["security", "performance", "testing", "documentation", "architecture", "dx", "dependencies"]
    title: str
    description: str
    priority: Literal["high", "medium", "low"]


class RepoAnalysis(BaseModel):
    repo_name: str
    summary: str
    main_purpose: str
    tech_stack: TechStack
    strengths: List[str]
    suggestions: List[Suggestion]
    overall_assessment: str
