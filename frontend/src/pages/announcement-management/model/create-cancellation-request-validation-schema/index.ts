import type { ICancellationRequestFields } from "@pages/announcement-management/model/create-cancellation-request-validation-schema/types";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createCancellationRequestValidationSchema = (t: TFunction): Yup.ObjectSchema<ICancellationRequestFields> =>
  Yup.object().shape({
    cancellation_reason: Yup.string()
      .trim()
      .max(256, t("validationErrors.maxLength", { maxLength: 256 })),
  });
