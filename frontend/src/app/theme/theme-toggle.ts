import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ThemeService } from './theme.service';

@Component({
  selector: 'theme-toggle',
  template: `<button mat-icon-button (click)="handleChangeTheme()">
    <mat-icon fontIcon="dark_mode" />
  </button>`,
  imports: [MatIconModule, MatButtonModule],
})
export class ThemeToggle {
  themeService = inject(ThemeService);

  handleChangeTheme() {
    this.themeService.toggleTheme();
  }
}
