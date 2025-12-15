import { HttpContext } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { SKIP_ERROR_HANDLING } from '@app/interceptors/error.interceptor';
import { TranslateService } from '@ngx-translate/core';
import { AuthApiService } from '@shared/api/auth/auth-api.service';
import { ILoginDto } from '@shared/api/auth/auth.types';
import { IUserDto } from '@shared/api/users/users-api.types';
import { EAuthErrorTypes } from '@shared/lib/auth/auth-error-types.const';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { IApiErrorResponse } from '@shared/lib/utility-types/api-errors.types';
import { catchError, EMPTY, finalize, map, of, switchMap, tap, throwError } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private authApiService = inject(AuthApiService);
  private router = inject(Router);
  private snackBarService = inject(SnackBarService);
  private translateService = inject(TranslateService);
  hasAttemptToLogin = false;
  accessToken = signal<TMaybe<string>>(null);
  me = signal<TMaybe<IUserDto>>(null);
  isAuthenticated = computed(() => Boolean(this.accessToken()));

  login = (params: ILoginDto) => {
    return this.authApiService.login(params).pipe(
      tap(({ access_token }) => {
        const successLoginText = this.translateService.instant('texts.successLogin');

        this.router.navigateByUrl('/games');
        this.setToken(access_token);
        this.snackBarService.showSuccessSnackBar(successLoginText);
        this.hasAttemptToLogin = true;
      }),
      switchMap(() => this.getMe()),
    );
  };

  logout = () => {
    this.authApiService
      .logout()
      .pipe(
        finalize(() => {
          this.hasAttemptToLogin = false;
          this.router.navigateByUrl('/login');
          this.accessToken.set(null);
          this.me.set(null);
        }),
      )
      .subscribe();
  };

  refreshToken = () => {
    return this.authApiService
      .refreshToken({ context: new HttpContext().set(SKIP_ERROR_HANDLING, true) })
      .pipe(
        tap(({ access_token }) => this.setToken(access_token)),
        catchError((response: IApiErrorResponse) => {
          const { error } = response;

          if (error.error_type === EAuthErrorTypes.TokenMissing) {
            return EMPTY;
          } else {
            this.logout();
            this.snackBarService.showErrorSnackBar(error.detail);

            return throwError(() => error);
          }
        }),
        switchMap((access_token) =>
          this.me() ? of(access_token) : this.getMe().pipe(map(() => access_token)),
        ),
        finalize(() => (this.hasAttemptToLogin = true)),
      );
  };

  getMe = () => {
    return this.authApiService.getMe().pipe(tap(({ data }) => this.me.set(data)));
  };

  private setToken = (token: string) => {
    this.accessToken.set(token);
  };
}
