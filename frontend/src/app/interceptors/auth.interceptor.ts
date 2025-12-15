import { HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { EAuthErrorTypes } from '@shared/lib/auth/auth-error-types.const';
import { AuthService } from '@shared/lib/auth/auth.service';
import { IApiErrorResponse } from '@shared/lib/utility-types/api-errors.types';
import { catchError, switchMap, throwError } from 'rxjs';

const getRequestWithToken = (request: HttpRequest<unknown>, accessToken: string) => {
  return request.clone({ setHeaders: { Authorization: `Bearer ${accessToken}` } });
};

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const accessToken = authService.accessToken();
  const hasAttemptToLogin = authService.hasAttemptToLogin;
  const authRequest = accessToken ? getRequestWithToken(request, accessToken) : request;

  return next(authRequest).pipe(
    catchError((response: IApiErrorResponse) => {
      const { status, error } = response;
      const { error_type } = error;

      if (status === 401) {
        if (error_type === EAuthErrorTypes.TokenExpired) {
          if (hasAttemptToLogin && !accessToken) {
            router.navigateByUrl('/login');

            return throwError(() => response);
          }

          return authService
            .refreshToken()
            .pipe(
              switchMap(({ access_token }) => next(getRequestWithToken(request, access_token))),
            );
        }
      }

      return throwError(() => response);
    }),
  );
};
