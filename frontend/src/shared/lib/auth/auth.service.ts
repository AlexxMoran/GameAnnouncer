import { HttpContext } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { SKIP_ERROR_HANDLING } from '@app/interceptors/error.interceptor';
import { ILoginDto } from '@shared/api/auth/auth-api-service.types';
import { AuthApiService } from '@shared/api/auth/auth-api.service';
import { IUserDto } from '@shared/api/users/users-api.types';
import { EAuthErrorTypes } from '@shared/lib/auth/auth-error-types.constants';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { IApiErrorResponse } from '@shared/lib/utility-types/api-errors.types';
import { EAppRoutes } from '@shared/routes/routes.constants';
import { catchError, EMPTY, finalize, map, of, switchMap, tap, throwError } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private authApiService = inject(AuthApiService);
  private router = inject(Router);
  private snackBarService = inject(SnackBarService);
  accessToken = signal<TMaybe<string>>(null);
  me = signal<TMaybe<IUserDto>>(null);
  isAuthenticated = computed(() => Boolean(this.accessToken()));

  login = (params: ILoginDto) => {
    return this.authApiService.login(params).pipe(
      tap(({ access_token }) => this.setToken(access_token)),
      switchMap(() =>
        this.getMe().pipe(
          tap(() => {
            this.snackBarService.showSuccessSnackBar('texts.successLogin');
            this.router.navigateByUrl(EAppRoutes.Games);
          }),
        ),
      ),
    );
  };

  logout = () => {
    this.authApiService
      .logout()
      .pipe(
        finalize(() => {
          this.router.navigateByUrl(EAppRoutes.Login);
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
            this.snackBarService.showErrorSnackBar(error.detail);
            this.logout();

            return throwError(() => error);
          }
        }),
        switchMap((access_token) =>
          this.me() ? of(access_token) : this.getMe().pipe(map(() => access_token)),
        ),
      );
  };

  getMe = () => {
    return this.authApiService.getMe().pipe(tap(({ data }) => this.me.set(data)));
  };

  private setToken = (token: string) => {
    this.accessToken.set(token);
  };
}
