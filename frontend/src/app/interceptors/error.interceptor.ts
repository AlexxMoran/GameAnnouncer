import { HttpContextToken, HttpInterceptorFn } from '@angular/common/http';
import { IApiErrorResponse } from '@shared/lib/api/error.types';
import { catchError, throwError } from 'rxjs';

export const SKIP_ERROR_HANDLING = new HttpContextToken<boolean>(() => false);

export const errorInterceptor: HttpInterceptorFn = (request, next) => {
  return next(request).pipe(
    catchError((response: IApiErrorResponse) => {
      if (request.context.get(SKIP_ERROR_HANDLING)) {
        return throwError(() => response);
      }

      return throwError(() => response);
    }),
  );
};
