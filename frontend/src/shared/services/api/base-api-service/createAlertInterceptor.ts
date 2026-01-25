import type { IApiConfig } from "@shared/services/api/base-api-service/types";
import type { TApiError } from "@shared/types/apiError.types";

export const createAlertErrorInterceptor = (
  alertError?: (message: string) => void
) => {
  return (error: TApiError) => {
    const { status, config, response } = error;
    const { suppressErrorHandling } = config as IApiConfig;

    if (suppressErrorHandling || error.code === "ERR_CANCELED") {
      return Promise.reject(response);
    }

    if (response && status) {
      const { data } = response;
      const { detail, message } = data;
      const errorText = message || detail || "Непредвиденная ошибка";
      // TODO перевести тексты
      switch (status) {
        case 401: {
          alertError?.("Не авторизован");

          break;
        }

        case 403: {
          alertError?.("Недостаточно прав");

          break;
        }

        case 404: {
          if (!detail && !message) {
            alertError?.("Не найдено");
          } else {
            alertError?.(errorText);
          }

          break;
        }

        default: {
          if (status >= 500) {
            alertError?.("Ошибка сервера");
          } else {
            alertError?.(errorText);
          }
        }
      }
    } else {
      alertError?.("Проверьте подключение к сети");
    }

    return Promise.reject(response);
  };
};
