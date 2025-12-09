import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { TranslatePipe } from '@ngx-translate/core';
import { LangToggle } from '@shared/ui/lang-toggle/lang-toggle';
import { ThemeToggle } from '@shared/ui/theme-toggle/theme-toggle';

@Component({
  selector: 'app-layout',
  imports: [ThemeToggle, LangToggle, RouterOutlet, TranslatePipe, RouterModule],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
  host: { class: 'w-full h-full flex flex-col' },
})
export class Layout {}
