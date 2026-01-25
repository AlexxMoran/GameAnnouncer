import type { AxiosError } from "axios";

export interface IApiBaseError {
  detail: string;
  message?: string;
  error_type?: string;
}

export type TApiError = AxiosError<IApiBaseError>;
