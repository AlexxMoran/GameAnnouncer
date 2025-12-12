import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
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

  get<TResponse, TMeta = unknown>(url: string, queryParams?: TObjectAny) {
    return this.httpClient.get<TResponse & TMeta>(
      `${this.apiUrl}${url}`,
      this.prepareQueryParams(queryParams),
    );
  }

  post<TResponse>(url: string, body?: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.post<TResponse>(`${this.apiUrl}${url}`, body, queryParams);
  }

  put<TResponse>(url: string, body: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.put<TResponse>(`${this.apiUrl}${url}`, body, queryParams);
  }

  patch<TResponse>(url: string, body: TObjectAny, queryParams?: TObjectAny) {
    return this.httpClient.patch<TResponse>(`${this.apiUrl}${url}`, body, queryParams);
  }

  delete<TResponse>(url: string, queryParams?: TObjectAny) {
    return this.httpClient.delete<TResponse>(`${this.apiUrl}${url}`, queryParams);
  }
}
