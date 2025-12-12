import { HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AUTH_ENDPOINT } from '@shared/api/auth/auth-api.const';
import { IAccessToken, ILoginDto, IRegisterDto } from '@shared/api/auth/auth.types';
import { BaseApiService } from '@shared/api/base-api.service';
import { IUserDto } from '@shared/api/users/users-api.types';

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
      headers,
    });
  };

  getMe = () => {
    return this.baseApiService.get<IUserDto>(`${AUTH_ENDPOINT}/users/me`);
  };

  logout = () => {
    return this.baseApiService.post<IAccessToken>(`${AUTH_ENDPOINT}/logout`);
  };

  register = (params: IRegisterDto) => {
    return this.baseApiService.post<IUserDto>(`${AUTH_ENDPOINT}/register`, params);
  };

  refreshToken = () => {
    return this.baseApiService.post<IAccessToken>(`${AUTH_ENDPOINT}/jwt/refresh`);
  };
}
