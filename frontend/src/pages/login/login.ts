import { Component, inject, signal } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthForm } from '@features/auth/ui/auth-form/auth-form';
import { TranslatePipe } from '@ngx-translate/core';
import { ILoginDto } from '@shared/api/auth/auth.types';
import { AuthService } from '@shared/lib/auth/auth.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-login',
  imports: [AuthForm, RouterModule, TranslatePipe],
  templateUrl: './login.html',
  host: {
    class: 'flex flex-col justify-center items-center h-full',
  },
})
export class Login {
  private authService = inject(AuthService);
  isLoading = signal(false);

  login = (params: ILoginDto) => {
    this.isLoading.set(true);
    this.authService
      .login(params)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe();
  };
}
