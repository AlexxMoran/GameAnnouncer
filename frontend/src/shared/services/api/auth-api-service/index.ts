import { AUTH_ENDPOINT } from "@shared/services/api/auth-api-service/constants";
import type {
  IAccessToken,
  IEditUserDto,
  ILoginDto,
  IRegisterDto,
  IUserDto,
} from "@shared/services/api/auth-api-service/types";
import type { BaseApiService } from "@shared/services/api/base-api-service";
import type {
  IApiConfig,
  TApiResponseWrapper,
} from "@shared/services/api/base-api-service/types";
import axios from "axios";

export class AuthApiService {
  constructor(private baseApiService: BaseApiService) {}

  login = (params: ILoginDto) => {
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    };

    const body = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => body.set(key, value));

    return this.baseApiService.post<IAccessToken>(
      `${AUTH_ENDPOINT}/login`,
      body,
      {
        withCredentials: true,
        headers,
      }
    );
  };

  getMe = () => {
    return this.baseApiService.get<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/users/me`,
      { withCredentials: true }
    );
  };

  editMe = (params: IEditUserDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/users/me`,
      params,
      { withCredentials: true }
    );
  };

  logout = () => {
    return this.baseApiService.post<IAccessToken>(
      `${AUTH_ENDPOINT}/logout`,
      {},
      { withCredentials: true }
    );
  };

  verifyEmail = (token: string) => {
    const body = new URLSearchParams();

    body.set("token", token);

    return this.baseApiService.post<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/verify?${body}`
    );
  };

  register = (params: IRegisterDto) => {
    const body = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => body.set(key, value));

    return this.baseApiService.post<TApiResponseWrapper<IUserDto>>(
      `${AUTH_ENDPOINT}/register?${body}`
    );
  };

  refreshToken = (config?: IApiConfig) => {
    // чтоб не было циклических зависимостей
    // TODO разобраться с base_api
    return axios.post<IAccessToken>(
      `http://localhost:4200/api/auth/jwt/refresh`,
      {},
      { withCredentials: true, ...config }
    );
  };
}
