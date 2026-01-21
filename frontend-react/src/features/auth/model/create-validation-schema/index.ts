import type { IAuthFields } from "@features/auth/model/create-validation-schema/types";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createValidationSchema = (
  t: TFunction
): Yup.ObjectSchema<IAuthFields> =>
  Yup.object().shape({
    username: Yup.string()
      .trim()
      .email(t("validationErrors.email"))
      .required(t("validationErrors.required")),
    password: Yup.string()
      .trim()
      .min(8, t("validationErrors.minLength", { minLength: 8 }))
      .max(16, t("validationErrors.maxLength", { maxLength: 16 }))
      .required(t("validationErrors.required")),
  });
