import { HttpContextToken, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { IApiErrorResponse } from '@shared/lib/utility-types/api-errors.types';
import { catchError, throwError } from 'rxjs';

export const SKIP_ERROR_HANDLING = new HttpContextToken<boolean>(() => false);

export const errorInterceptor: HttpInterceptorFn = (request, next) => {
  const snackBarService = inject(SnackBarService);

  return next(request).pipe(
    catchError((response: IApiErrorResponse) => {
      if (request.context.get(SKIP_ERROR_HANDLING)) {
        return throwError(() => response);
      }

      const { error, message } = response;
      const { detail } = error;

      if (detail) {
        if (typeof detail === 'string') {
          snackBarService.showErrorSnackBar(detail);
        } else {
          detail.forEach(({ msg }) => snackBarService.showErrorSnackBar(msg));
        }
      } else {
        snackBarService.showErrorSnackBar(message);
      }

      return throwError(() => response);
    }),
  );
};
