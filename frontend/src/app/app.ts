import { Component } from '@angular/core';
import { LangToggle } from 'src/app/lang-toggle/lang-toggle';
import { ThemeToggle } from 'src/app/theme-toggle/theme-toggle';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  imports: [ThemeToggle, LangToggle],
  host: {
    class: 'w-screen h-screen flex flex-col',
  },
})
export class App {}
