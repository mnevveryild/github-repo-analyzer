import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AnalysisMode, RepoAnalysis, SystemDesignAnalysis } from '../models/analysis.model';

interface AnalyzeRequest {
  repo_url: string;
  mode: AnalysisMode;
}

@Injectable({ providedIn: 'root' })
export class AnalyzerService {
  private readonly apiUrl = '/api';

  constructor(private http: HttpClient) {}

  analyzeCodeReview(repoUrl: string): Observable<RepoAnalysis> {
    const body: AnalyzeRequest = { repo_url: repoUrl, mode: 'code_review' };
    return this.http.post<RepoAnalysis>(`${this.apiUrl}/analyze`, body);
  }

  analyzeSystemDesign(repoUrl: string): Observable<SystemDesignAnalysis> {
    const body: AnalyzeRequest = { repo_url: repoUrl, mode: 'system_design' };
    return this.http.post<SystemDesignAnalysis>(`${this.apiUrl}/analyze`, body);
  }
}
