import { Component, Input } from '@angular/core';
import { NgClass } from '@angular/common';
import { RepoAnalysis } from '../../models/analysis.model';

@Component({
  selector: 'app-code-review-result',
  standalone: true,
  imports: [NgClass],
  templateUrl: './code-review-result.component.html',
  styleUrl: './code-review-result.component.scss',
})
export class CodeReviewResultComponent {
  @Input({ required: true }) result!: RepoAnalysis;

  expanded: Record<string, boolean> = {
    techStack: true,
    strengths: true,
    suggestions: true,
  };

  toggle(section: string): void {
    this.expanded[section] = !this.expanded[section];
  }

  priorityClass(priority: string): string {
    const map: Record<string, string> = {
      high: 'priority-high',
      medium: 'priority-medium',
      low: 'priority-low',
    };
    return map[priority?.toLowerCase()] ?? 'priority-low';
  }

  categoryClass(category: string): string {
    const map: Record<string, string> = {
      security: 'cat-security',
      performance: 'cat-performance',
      testing: 'cat-testing',
      documentation: 'cat-documentation',
      architecture: 'cat-architecture',
      dx: 'cat-dx',
      dependencies: 'cat-dependencies',
    };
    return map[category?.toLowerCase()] ?? 'cat-default';
  }

  techEntries(): { label: string; items: string[] }[] {
    const ts = this.result.tech_stack;
    return [
      { label: 'Diller', items: ts.languages },
      { label: 'Frameworkler', items: ts.frameworks },
      { label: 'Veritabanlari', items: ts.databases },
      { label: 'Araclar', items: ts.tools },
      { label: 'Bulut', items: ts.cloud_services },
    ].filter((e) => e.items?.length > 0);
  }
}
