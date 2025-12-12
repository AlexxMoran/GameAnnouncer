import { Component, DOCUMENT, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { THEME_TYPE_STORAGE_NAME } from '@features/layout/ui/theme-toggle/theme-toggle.const';
import { TThemeType } from '@features/layout/ui/theme-toggle/theme-toggle.types';

@Component({
  selector: 'theme-toggle',
  templateUrl: './theme-toggle.html',
  imports: [MatIconModule, MatButtonModule],
})
export class ThemeToggle {
  document = inject(DOCUMENT);

  constructor() {
    this.init();
  }

  get currentTheme(): TThemeType {
    return (localStorage.getItem(THEME_TYPE_STORAGE_NAME) as TThemeType) || 'light';
  }

  setTheme(theme: TThemeType) {
    localStorage.setItem(THEME_TYPE_STORAGE_NAME, theme);
    this.document.body.style.setProperty('color-scheme', theme);
  }

  toggleTheme() {
    if (this.currentTheme === 'dark') {
      this.setTheme('light');
    } else {
      this.setTheme('dark');
    }
  }

  init() {
    const savedTheme = this.currentTheme;
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
      this.setTheme(savedTheme);
    } else if (systemPrefersDark) {
      this.setTheme('dark');
    }
  }
}
