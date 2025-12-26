import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { IHttpClientRequestOptions } from '@shared/api/base-api-service.types';
import { environment } from '@shared/config/environments/environment';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

@Injectable({ providedIn: 'root' })
export class BaseApiService {
  private httpClient = inject(HttpClient);

  private get apiUrl() {
    return environment.apiUrl;
  }

  private prepareQueryParams(queryParams?: TObjectAny) {
    return { params: new HttpParams({ fromObject: queryParams }) };
  }

  get<TResponse, TMeta = unknown>(url: string, options?: IHttpClientRequestOptions) {
    const { params, ...otherOptions } = options || {};

    return this.httpClient.get<TResponse & TMeta>(`${this.apiUrl}${url}`, {
      ...this.prepareQueryParams(params),
      ...otherOptions,
    });
  }

  post<TResponse>(url: string, body?: TObjectAny, options?: IHttpClientRequestOptions) {
    const { params, ...otherOptions } = options || {};

    return this.httpClient.post<TResponse>(`${this.apiUrl}${url}`, body, {
      ...this.prepareQueryParams(params),
      ...otherOptions,
    });
  }

  put<TResponse>(url: string, body: TObjectAny, options?: IHttpClientRequestOptions) {
    const { params, ...otherOptions } = options || {};

    return this.httpClient.put<TResponse>(`${this.apiUrl}${url}`, body, {
      ...this.prepareQueryParams(params),
      ...otherOptions,
    });
  }

  patch<TResponse>(url: string, body: TObjectAny, options?: IHttpClientRequestOptions) {
    const { params, ...otherOptions } = options || {};

    return this.httpClient.patch<TResponse>(`${this.apiUrl}${url}`, body, {
      ...this.prepareQueryParams(params),
      ...otherOptions,
    });
  }

  delete<TResponse>(url: string, options?: IHttpClientRequestOptions) {
    const { params, ...otherOptions } = options || {};

    return this.httpClient.delete<TResponse>(`${this.apiUrl}${url}`, {
      ...this.prepareQueryParams(params),
      ...otherOptions,
    });
  }
}
