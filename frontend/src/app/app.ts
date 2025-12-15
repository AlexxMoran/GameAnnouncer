import { Component, inject, signal } from '@angular/core';
import { MatProgressSpinner } from '@angular/material/progress-spinner';
import { Layout } from '@app/layout/layout';
import { AuthService } from '@shared/lib/auth/auth.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  imports: [Layout, MatProgressSpinner],
})
export class App {
  authService = inject(AuthService);
  isAppInitialized = signal(false);

  constructor() {
    this.initApp();
  }

  initApp = () => {
    this.authService
      .refreshToken()
      .pipe(finalize(() => this.isAppInitialized.set(true)))
      .subscribe();
  };
}
