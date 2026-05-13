import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AnalyzerService } from '../../services/analyzer.service';
import { RepoAnalysis, SystemDesignAnalysis } from '../../models/analysis.model';
import { CodeReviewResultComponent } from '../code-review-result/code-review-result.component';
import { SystemDesignResultComponent } from '../system-design-result/system-design-result.component';

type Mode = 'code_review' | 'system_design';

@Component({
  selector: 'app-analyzer-form',
  standalone: true,
  imports: [CommonModule, FormsModule, CodeReviewResultComponent, SystemDesignResultComponent],
  templateUrl: './analyzer-form.component.html',
  styleUrl: './analyzer-form.component.scss',
})
export class AnalyzerFormComponent {
  repoUrl = '';
  mode: Mode = 'code_review';
  loading = false;
  error: string | null = null;
  codeReviewResult: RepoAnalysis | null = null;
  systemDesignResult: SystemDesignAnalysis | null = null;

  constructor(private analyzerService: AnalyzerService) {}

  onSubmit(): void {
    if (!this.repoUrl.trim() || this.loading) return;

    this.loading = true;
    this.error = null;
    this.codeReviewResult = null;
    this.systemDesignResult = null;

    if (this.mode === 'code_review') {
      this.analyzerService.analyzeCodeReview(this.repoUrl.trim()).subscribe({
        next: (result) => {
          this.loading = false;
          this.codeReviewResult = result;
        },
        error: (err) => {
          this.loading = false;
          this.error = err.error?.detail ?? 'Analiz sirasinda bir hata olustu.';
        },
      });
    } else {
      this.analyzerService.analyzeSystemDesign(this.repoUrl.trim()).subscribe({
        next: (result) => {
          this.loading = false;
          this.systemDesignResult = result;
        },
        error: (err) => {
          this.loading = false;
          this.error = err.error?.detail ?? 'Analiz sirasinda bir hata olustu.';
        },
      });
    }
  }
}
