import type { IRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields/types";
import type { FormikErrors } from "formik";
import type { TFunction } from "i18next";
import isEmpty from "lodash/isEmpty";

export const validateRegistrationFormFields = ({ fields }: IRegistrationFormFields, t: TFunction) => {
  const validationErrors = Object.entries(fields || {}).reduce<FormikErrors<IRegistrationFormFields>>(
    (acc, [key, { field_type, options, label }]) => {
      const typeError = field_type ? "" : t("validationErrors.required");
      const labelError = label ? "" : t("validationErrors.required");

      const optionsErrors = Object.entries(options || {}).reduce<Record<string, string>>((acc, [key, value]) => {
        if (typeof value === "string" && !value) {
          acc[key] = t("validationErrors.required");
        }

        return acc;
      }, {});

      if (typeError || labelError || !isEmpty(optionsErrors)) {
        if (acc["fields"]) {
          acc["fields"][key] = { field_type: typeError, label: labelError, options: JSON.stringify(optionsErrors) };
        }
      }

      return acc;
    },
    { fields: {} }
  );

  if (!isEmpty(validationErrors.fields)) {
    return validationErrors;
  }
};
