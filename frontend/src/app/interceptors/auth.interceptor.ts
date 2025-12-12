import { HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '@shared/lib/auth/auth.service';
import { IApiErrorResponse } from '@shared/lib/utility-types/api-errors.types';
import { catchError, switchMap, throwError } from 'rxjs';

const getRequestWithToken = (request: HttpRequest<unknown>, accessToken: string) => {
  return request.clone({ setHeaders: { Authorization: `Bearer ${accessToken}` } });
};

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);
  const accessToken = authService.getAccessToken();
  const authRequest = accessToken ? getRequestWithToken(request, accessToken) : request;

  return next(authRequest).pipe(
    catchError((response: IApiErrorResponse) => {
      const { status, error } = response;
      const { detail } = error;

      if (status === 401 && detail === 'Unauthorized') {
        return authService
          .refreshToken()
          .pipe(switchMap(({ access_token }) => next(getRequestWithToken(request, access_token))));
      }

      return throwError(() => response);
    }),
  );
};
