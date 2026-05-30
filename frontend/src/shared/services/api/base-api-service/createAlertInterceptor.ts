import i18n from "@shared/config/i18n/config";
import type { IApiConfig } from "@shared/services/api/base-api-service/types";
import type {
  IApiStructuredError,
  TApiError,
  TApiErrorParams,
} from "@shared/types/apiError.types";

const translateApiMessage = (messageKey?: string, params?: TApiErrorParams) => {
  if (!messageKey) {
    return "";
  }

  return i18n.t(`apiErrors.${messageKey}`, { ...params, defaultValue: "" });
};

const translateStructuredErrors = (errors?: IApiStructuredError[]) => {
  if (!errors?.length) {
    return "";
  }

  return errors
    .map((error) => translateApiMessage(error.message_key, error.params) || error.message)
    .filter(Boolean)
    .join("; ");
};

export const createAlertErrorInterceptor = (alertError?: (message: string) => void) => {
  return (error: TApiError) => {
    const { status, config, response } = error;
    const { suppressErrorHandling } = config as IApiConfig;

    if (suppressErrorHandling || error.code === "ERR_CANCELED") {
      return Promise.reject(response);
    }

    if (response && status) {
      const { data } = response;
      const { detail, message, message_key, errors } = data;

      const structuredErrorText = translateStructuredErrors(errors);
      const localizedMessage = translateApiMessage(message_key);
      const errorText =
        structuredErrorText || localizedMessage || message || detail || i18n.t("validationErrors.unknown");

      switch (status) {
        case 401: {
          alertError?.(i18n.t("apiErrors.unauthorized"));
          break;
        }

        case 403: {
          alertError?.(i18n.t("apiErrors.forbidden"));
          break;
        }

        default: {
          if (status >= 500) {
            alertError?.(i18n.t("apiErrors.server_error"));
          } else {
            alertError?.(errorText);
          }
        }
      }
    } else {
      alertError?.(i18n.t("apiErrors.network_error"));
    }

    return Promise.reject(response);
  };
};
