import { Component, inject } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { RouterModule, RouterOutlet } from '@angular/router';
import { LangToggle } from '@features/layout/ui/lang-toggle/lang-toggle';
import { ThemeToggle } from '@features/layout/ui/theme-toggle/theme-toggle';
import { UserInfo } from '@features/layout/ui/user-info/user-info';
import { TranslatePipe } from '@ngx-translate/core';
import { AuthService } from '@shared/lib/auth/auth.service';
import { EAppRoutes } from '@shared/routes/routes.constants';

@Component({
  selector: 'app-layout',
  imports: [
    MatProgressSpinnerModule,
    ThemeToggle,
    LangToggle,
    RouterOutlet,
    TranslatePipe,
    RouterModule,
    UserInfo,
  ],
  templateUrl: './layout.html',
  host: { class: 'w-full h-full flex flex-col' },
})
export class Layout {
  private authService = inject(AuthService);

  get isAuthenticated() {
    return this.authService.isAuthenticated();
  }

  get routes() {
    return {
      login: EAppRoutes.Login,
      games: EAppRoutes.Games,
      announcements: EAppRoutes.Announcements,
    };
  }

  get me() {
    return this.authService.me();
  }
}
