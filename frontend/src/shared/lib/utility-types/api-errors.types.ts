import { HttpErrorResponse } from '@angular/common/http';

export interface IApiBaseError {
  detail: string;
  message?: string;
}

export interface IApiValidationErrorDetail {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface IApiValidationError {
  detail: IApiValidationErrorDetail[];
}

export type TApiError = IApiBaseError | IApiValidationError;

export interface IApiErrorResponse extends HttpErrorResponse {
  error: TApiError;
  status: number;
}
