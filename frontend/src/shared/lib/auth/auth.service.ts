import { inject, Injectable, signal } from '@angular/core';
import { BaseApiService } from '@shared/lib/api/base-api.service';
import { AUTH_ENDPOINT } from '@shared/lib/auth/auth.const';
import { IAccessToken, ILoginParams } from '@shared/lib/auth/auth.types';
import { TMaybe } from '@shared/lib/utility-types/additional.types';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseApiService = inject(BaseApiService);
  accessToken = signal<TMaybe<string>>(null);

  login(params: ILoginParams) {
    this.baseApiService.post<IAccessToken>(`${AUTH_ENDPOINT}/login`, params);
  }
}
