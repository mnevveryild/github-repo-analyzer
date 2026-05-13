import { Component } from '@angular/core';
import { AnalyzerFormComponent } from './components/analyzer-form/analyzer-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AnalyzerFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {}
