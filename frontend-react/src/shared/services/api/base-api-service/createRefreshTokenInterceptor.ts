import type { TApiError } from "@shared/types/apiError.types";
import type { AxiosInstance } from "axios";

export const createRefreshTokenInterceptor = (
  axiosInstance: AxiosInstance,
  refreshToken?: () => Promise<string | undefined>,
  redirectToLogin?: () => void
) => {
  return async (error: TApiError) => {
    const { status, config, response } = error;

    if (response) {
      const { data } = response;
      const { error_type } = data;

      if (status === 401 && error_type === "token_expired") {
        try {
          const token = await refreshToken?.();

          if (config) {
            config.headers["Authorization"] = `Bearer ${token}`;

            return axiosInstance(config);
          }
        } catch (_) {
          redirectToLogin?.();

          return Promise.reject(error);
        }
      }

      return Promise.reject(error);
    }

    return Promise.reject(error);
  };
};
