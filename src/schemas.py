from typing import List, Literal, Dict
from pydantic import BaseModel


# ── Mevcut modeller (değişmedi) ────────────────────────────────────────────────

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


# ── Yeni modeller (System Design modu) ────────────────────────────────────────

class RoadmapStep(BaseModel):
    phase: str          # Örn: "Aşama 1: Temel Altyapı"
    duration: str       # Örn: "1-2 hafta"
    tasks: List[str]    # Bu aşamada yapılacaklar
    deliverable: str    # Bu aşama sonunda elde edilecek çıktı


class SystemDesignAnalysis(BaseModel):
    repo_name: str
    summary: str                                    # Projenin 2-3 cümlelik özeti
    core_features: List[str]                        # Temel özellikler listesi
    recommended_tech_stack: Dict[str, List[str]]    # {"Frontend": [...], "Backend": [...], ...}
    step_by_step_roadmap: List[RoadmapStep]         # Aşamalı geliştirme planı
    potential_challenges: List[str]                 # Karşılaşılabilecek zorluklar
    estimated_total_duration: str                   # Örn: "3-4 ay"