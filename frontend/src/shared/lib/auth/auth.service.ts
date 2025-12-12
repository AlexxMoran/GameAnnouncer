import { computed, effect, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { AuthApiService } from '@shared/api/auth/auth-api.service';
import { ILoginDto } from '@shared/api/auth/auth.types';
import { IUserDto } from '@shared/api/users/users-api.types';
import { STORAGE_TOKEN_KEY } from '@shared/lib/auth/storage.const';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { catchError, finalize, tap, throwError } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private authApiService = inject(AuthApiService);
  private router = inject(Router);
  private snackBarService = inject(SnackBarService);
  private translateService = inject(TranslateService);
  private accessToken = signal<TMaybe<string>>(null);
  me = signal<TMaybe<IUserDto>>(null);
  isMeLoading = signal(false);
  hasToken = computed(() => Boolean(this.getAccessToken()));

  constructor() {
    effect(() => {
      if (this.hasToken()) {
        this.isMeLoading.set(true);
        this.authApiService
          .getMe()
          .pipe(finalize(() => this.isMeLoading.set(false)))
          .subscribe({ next: (me) => this.me.set(me) });
      } else {
        this.me.set(null);
      }
    });
  }

  get hasMe() {
    return !!this.me();
  }

  login = (params: ILoginDto) => {
    return this.authApiService.login(params).pipe(
      tap(({ access_token }) => {
        const successLoginText = this.translateService.instant('texts.successLogin');
        this.router.navigateByUrl('/games');
        this.setToken(access_token);
        this.snackBarService.showSuccessSnackBar(successLoginText);
      }),
    );
  };

  logout = () => {
    this.authApiService
      .logout()
      .pipe(
        finalize(() => {
          localStorage.removeItem(STORAGE_TOKEN_KEY);
          this.router.navigateByUrl('/login');
          this.accessToken.set(null);
        }),
      )
      .subscribe();
  };

  refreshToken = () => {
    return this.authApiService.refreshToken().pipe(
      tap(({ access_token }) => this.setToken(access_token)),
      catchError((error) => {
        this.logout();

        return throwError(() => error);
      }),
    );
  };

  private setTokenInStorage = (token: string) => {
    localStorage.setItem(STORAGE_TOKEN_KEY, token);
  };

  private getTokenFromStorage = () => {
    return localStorage.getItem(STORAGE_TOKEN_KEY);
  };

  private setToken = (token: string) => {
    this.accessToken.set(token);
    this.setTokenInStorage(token);
  };

  getAccessToken = () => {
    return this.accessToken() || this.getTokenFromStorage();
  };
}
