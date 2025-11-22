import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LangToggle } from '@shared/ui/lang-toggle/lang-toggle';
import { ThemeToggle } from '@shared/ui/theme-toggle/theme-toggle';

@Component({
  selector: 'app-layout',
  imports: [ThemeToggle, LangToggle, RouterOutlet],
  templateUrl: './app-layout.html',
  styleUrl: './app-layout.scss',
})
export class AppLayout {}
