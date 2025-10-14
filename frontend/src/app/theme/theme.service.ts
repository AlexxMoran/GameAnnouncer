import { DOCUMENT } from '@angular/common';
import { inject, Injectable } from '@angular/core';
import { THEME_TYPE_STORAGE_NAME } from './theme.constants';
import { TThemeType } from './theme.types';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
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
