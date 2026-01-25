import { createAddTokenInterceptor } from "@shared/services/api/base-api-service/createAddTokenInterceptor";
import { createAlertErrorInterceptor } from "@shared/services/api/base-api-service/createAlertInterceptor";
import { createRefreshTokenInterceptor } from "@shared/services/api/base-api-service/createRefreshTokenInterceptor";
import type { IApiConfig } from "@shared/services/api/base-api-service/types";
import type { AuthService } from "@shared/services/auth-service";
import type { IRootServiceData } from "@shared/services/root-service/types";
import type { TObjectAny } from "@shared/types/main.types";
import axios from "axios";

// TODO добавить сериализацию параметров
// TODO добавить abort для запросов при unmount компонента

export class BaseApiService {
  private axiosInstance = axios.create({ baseURL: "/api" });

  createInterceptors = (data: IRootServiceData, authService: AuthService) => {
    const { alertError, redirectToLoginPage } = data;

    this.axiosInstance.interceptors.response.use(
      null,
      createRefreshTokenInterceptor(
        this.axiosInstance,
        authService.refreshToken,
        redirectToLoginPage
      )
    );

    this.axiosInstance.interceptors.response.use(
      null,
      createAlertErrorInterceptor(alertError)
    );

    this.axiosInstance.interceptors.request.use(
      createAddTokenInterceptor(authService)
    );
  };

  get<TResponse, TMeta = unknown>(url: string, config?: IApiConfig) {
    return this.axiosInstance.get<TResponse & TMeta>(url, config);
  }

  post<TResponse>(url: string, body?: TObjectAny, config?: IApiConfig) {
    return this.axiosInstance.post<TResponse>(url, body, config);
  }

  put<TResponse>(url: string, body: TObjectAny, config?: IApiConfig) {
    return this.axiosInstance.put<TResponse>(url, body, config);
  }

  patch<TResponse>(url: string, body: TObjectAny, config?: IApiConfig) {
    return this.axiosInstance.patch<TResponse>(url, body, config);
  }

  delete<TResponse>(url: string, config?: IApiConfig) {
    return this.axiosInstance.delete<TResponse>(url, config);
  }
}
