import { Component } from '@angular/core';
import { ThemeToggle } from './theme/theme-toggle';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  imports: [ThemeToggle],
  host: {
    class: 'w-screen h-screen flex flex-col',
  },
})
export class App {}
