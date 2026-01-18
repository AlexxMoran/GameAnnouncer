import type { ICreateGameFields } from "@pages/games/model/create-validation-schema/types";
import type { EGameCategories } from "@shared/services/api/games-api-service/constants";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createValidationSchema = (
  t: TFunction
): Yup.ObjectSchema<ICreateGameFields> =>
  Yup.object().shape({
    name: Yup.string()
      .trim()
      .max(64, t("validationErrors.maxLength", { maxLength: 64 }))
      .required(t("validationErrors.required")),
    description: Yup.string()
      .trim()
      .min(8, t("validationErrors.minLength", { minLength: 8 }))
      .max(256, t("validationErrors.maxLength", { maxLength: 256 }))
      .required(t("validationErrors.required")),
    category: Yup.string<EGameCategories>()
      .trim()
      .required(t("validationErrors.required")),
  });
