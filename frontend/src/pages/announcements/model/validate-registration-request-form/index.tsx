import type { IRegistrationFormFieldWithId } from "@shared/services/api/announcements-api-service/types";
import type { FormikErrors } from "formik";
import type { TFunction } from "i18next";

export const validateRegistrationRequestForm = (
  fieldList: IRegistrationFormFieldWithId[],
  values: Record<string, string | boolean>,
  t: TFunction
) => {
  const validationErrors = {} as FormikErrors<Record<string, string | boolean>>;

  const fields = fieldList.reduce<Record<string, IRegistrationFormFieldWithId>>((acc, field) => {
    acc[field.id] = field;

    return acc;
  }, {});

  Object.entries(values).forEach(([key, value]) => {
    const field = fields[key];

    if (field && field.required && !value) {
      validationErrors[key] = t("validationErrors.required");
    }
  });

  return validationErrors;
};
