import { HttpContext, HttpHeaders } from '@angular/common/http';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

export interface TApiResponseWrapper<TResponse> {
  data: TResponse;
}

export interface IHttpClientRequestOptions {
  headers?: HttpHeaders | Record<string, string | string[]>;
  params?: TObjectAny;
  withCredentials?: boolean;
  context?: HttpContext;
}
