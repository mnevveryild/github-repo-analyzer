import { Component, Input } from '@angular/core';
import { NgStyle } from '@angular/common';
import { SystemDesignAnalysis } from '../../models/analysis.model';

@Component({
  selector: 'app-system-design-result',
  standalone: true,
  imports: [NgStyle],
  templateUrl: './system-design-result.component.html',
  styleUrl: './system-design-result.component.scss',
})
export class SystemDesignResultComponent {
  @Input({ required: true }) result!: SystemDesignAnalysis;

  expanded: Record<string, boolean> = {
    features: true,
    techStack: true,
    roadmap: true,
    challenges: true,
  };

  toggle(section: string): void {
    this.expanded[section] = !this.expanded[section];
  }

  phaseColor(phase: number): string {
    const colors = ['#9b6dbf', '#c4968c', '#5090d0', '#4caf82', '#f0a050', '#e05555'];
    return colors[(phase - 1) % colors.length];
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
