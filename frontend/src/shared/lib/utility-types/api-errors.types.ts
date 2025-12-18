import { HttpErrorResponse } from '@angular/common/http';

export interface IApiBaseError {
  detail: string;
  message?: string;
  error_type?: string;
}

export interface IApiErrorResponse extends HttpErrorResponse {
  error: IApiBaseError;
  status: number;
}
