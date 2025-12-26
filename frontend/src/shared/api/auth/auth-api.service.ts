import { HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { IAccessToken, ILoginDto, IRegisterDto } from '@shared/api/auth/auth-api-service.types';
import { IHttpClientRequestOptions, TApiResponseWrapper } from '@shared/api/base-api-service.types';
import { BaseApiService } from '@shared/api/base-api.service';
import { IUserDto } from '@shared/api/users/users-api.types';

const AUTH_ENDPOINT = '/api/auth';

@Injectable({ providedIn: 'root' })
export class AuthApiService {
  private baseApiService = inject(BaseApiService);

  login = (params: ILoginDto) => {
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
      Accept: 'application/json',
    });

    const body = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => body.set(key, value));

    return this.baseApiService.post<IAccessToken>(`${AUTH_ENDPOINT}/login`, body, {
      withCredentials: true,
      headers,
    });
  };

  getMe = () => {
    return this.baseApiService.get<TApiResponseWrapper<IUserDto>>(`${AUTH_ENDPOINT}/users/me`);
  };

  logout = () => {
    return this.baseApiService.post<IAccessToken>(
      `${AUTH_ENDPOINT}/logout`,
      {},
      { withCredentials: true },
    );
  };

  verifyEmail = (token: string) => {
    const body = new URLSearchParams();

    body.set('token', token);

    return this.baseApiService.post<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/verify?${body}`,
    );
  };

  register = (params: IRegisterDto) => {
    const body = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => body.set(key, value));

    return this.baseApiService.post<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/register?${body}`,
    );
  };

  refreshToken = (options?: IHttpClientRequestOptions) => {
    return this.baseApiService.post<IAccessToken>(
      `${AUTH_ENDPOINT}/jwt/refresh`,
      {},
      { withCredentials: true, ...options },
    );
  };
}
