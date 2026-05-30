import type { AxiosError } from "axios";

export type TApiErrorParams = Record<string, string | number | boolean | null>;

export interface IApiStructuredError {
  field?: string;
  message?: string;
  message_key: string;
  params?: TApiErrorParams;
}

export interface IApiBaseError {
  detail: string;
  message?: string;
  error_type?: string;
  message_key?: string;
  errors?: IApiStructuredError[];
}

export type TApiError = AxiosError<IApiBaseError>;
