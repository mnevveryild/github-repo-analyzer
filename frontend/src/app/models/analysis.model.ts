export interface TechStack {
  languages: string[];
  frameworks: string[];
  databases: string[];
  tools: string[];
  cloud_services: string[];
}

export interface Suggestion {
  category: string;
  title: string;
  description: string;
  priority: string;
}

export interface RepoAnalysis {
  repo_name: string;
  description: string;
  summary: string;
  tech_stack: TechStack;
  strengths: string[];
  suggestions: Suggestion[];
  overall_assessment: string;
}

export interface RoadmapStep {
  phase: number;
  title: string;
  tasks: string[];
  deliverables: string[];
  estimated_duration: string;
}

export interface SystemDesignAnalysis {
  repo_name: string;
  description: string;
  core_features: string[];
  tech_stack: TechStack;
  roadmap: RoadmapStep[];
  potential_challenges: string[];
  total_estimated_duration: string;
}

export type AnalysisMode = 'code_review' | 'system_design';
