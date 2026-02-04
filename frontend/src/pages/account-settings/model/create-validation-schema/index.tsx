import type { IEditUserDto } from "@shared/services/api/auth-api-service/types";
import type { TFunction } from "i18next";
import * as Yup from "yup";

export const createValidationSchema = <TName extends keyof IEditUserDto>(
  name: TName,
  t: TFunction
): Yup.ObjectSchema<Record<TName, string>> =>
  Yup.object().shape({
    [name]: Yup.string()
      .trim()
      .max(32, t("validationErrors.maxLength", { maxLength: 32 })),
  }) as Yup.ObjectSchema<Record<TName, string>>;
