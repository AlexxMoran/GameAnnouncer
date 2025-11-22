import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '@shared/config/environments/environment';
import { IPagenationMeta } from '@shared/lib/api/offset-pagination.types';
import { TObjectAny } from '@shared/lib/utility-types/object.types';

export type TApiResponseWrapper<TResponse, TWithOffesetPaginationMeta extends boolean = false> = {
  data: TResponse;
} & (TWithOffesetPaginationMeta extends true ? IPagenationMeta : unknown);

@Injectable({ providedIn: 'root' })
export class BaseApiService {
  httpClient = inject(HttpClient);

  get apiUrl() {
    return environment.apiUrl;
  }

  get<TResponse, TWithOffesetPaginationMeta extends boolean = false>(
    url: string,
    queryParams?: TObjectAny,
  ) {
    return this.httpClient.get<TApiResponseWrapper<TResponse, TWithOffesetPaginationMeta>>(
      `${this.apiUrl}${url}`,
      this.prepareQueryParams(queryParams),
    );
  }

  post<TResponse>(url: string, body: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.post<TApiResponseWrapper<TResponse>>(
      `${this.apiUrl}${url}`,
      body,
      this.prepareQueryParams(queryParams),
    );
  }

  put<TResponse>(url: string, body: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.put<TApiResponseWrapper<TResponse>>(
      `${this.apiUrl}${url}`,
      body,
      this.prepareQueryParams(queryParams),
    );
  }

  patch<TResponse>(url: string, body: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.patch<TApiResponseWrapper<TResponse>>(
      `${this.apiUrl}${url}`,
      body,
      this.prepareQueryParams(queryParams),
    );
  }

  delete<TResponse>(url: string, queryParams?: TObjectAny) {
    return this.httpClient.delete<TApiResponseWrapper<TResponse>>(
      `${this.apiUrl}${url}`,
      this.prepareQueryParams(queryParams),
    );
  }

  private prepareQueryParams(queryParams?: TObjectAny) {
    return { params: new HttpParams({ fromObject: queryParams }) };
  }
}
