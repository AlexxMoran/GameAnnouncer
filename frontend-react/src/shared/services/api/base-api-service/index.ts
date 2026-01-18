import type { IApiConfig } from "@shared/services/api/base-api-service/types";
import type { TObjectAny } from "@shared/types/main.types";
import axios from "axios";

// TODO добавить сериализацию параметров

export class BaseApiService {
  axiosInstance = axios.create({ baseURL: "/api" });
  private abortControllers = new Map<string, AbortController>();

  private createRequestKey(url: string, method: string) {
    return `${method}:${url}`;
  }

  private async makeRequest<T>(
    requestFn: (signal: AbortSignal) => Promise<T>,
    url: string,
    method: string
  ): Promise<T> {
    const key = this.createRequestKey(url, method);

    this.cancelRequest(url, method);

    const controller = new AbortController();
    this.abortControllers.set(key, controller);

    try {
      return await requestFn(controller.signal);
    } finally {
      this.abortControllers.delete(key);
    }
  }

  private cancelRequest(url: string, method: string): void {
    const key = this.createRequestKey(url, method);
    const controller = this.abortControllers.get(key);

    if (controller) {
      controller.abort();
      this.abortControllers.delete(key);
    }
  }

  cancelAllRequests = () => {
    this.abortControllers.forEach((controller) => controller.abort());
    this.abortControllers.clear();
  };

  get<TResponse, TMeta = unknown>(url: string, config?: IApiConfig) {
    return this.makeRequest(
      (signal) =>
        this.axiosInstance.get<TResponse & TMeta>(url, {
          ...config,
          signal,
        }),
      url,
      "GET"
    );
  }

  post<TResponse>(url: string, body?: TObjectAny, config?: IApiConfig) {
    return this.makeRequest(
      (signal) =>
        this.axiosInstance.post<TResponse>(url, body, {
          ...config,
          signal,
        }),
      url,
      "POST"
    );
  }

  put<TResponse>(url: string, body: TObjectAny, config?: IApiConfig) {
    return this.makeRequest(
      (signal) =>
        this.axiosInstance.put<TResponse>(url, body, {
          ...config,
          signal,
        }),
      url,
      "PUT"
    );
  }

  patch<TResponse>(url: string, body: TObjectAny, config?: IApiConfig) {
    return this.makeRequest(
      (signal) =>
        this.axiosInstance.patch<TResponse>(url, body, {
          ...config,
          signal,
        }),
      url,
      "PATCH"
    );
  }

  delete<TResponse>(url: string, config?: IApiConfig) {
    return this.makeRequest(
      (signal) =>
        this.axiosInstance.delete<TResponse>(url, {
          ...config,
          signal,
        }),
      url,
      "DELETE"
    );
  }
}
