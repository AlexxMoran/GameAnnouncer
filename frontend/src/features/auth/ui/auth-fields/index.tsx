import type { IAuthFields } from "@features/auth/model/create-validation-schema/types";
import { TextField } from "@shared/ui/text-field";
import { useFormikContext } from "formik";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AuthFields: FC = () => {
  const { t } = useTranslation();
  const { errors, values, handleChange } = useFormikContext<IAuthFields>();

  return (
    <>
      <TextField
        name="username"
        label={t("entities.email")}
        onChange={handleChange}
        value={values["username"]}
        error={!!errors["username"]}
        helperText={errors["username"]}
        required
      />
      <TextField
        name="password"
        label={t("entities.password")}
        placeholder={t("placeholders:enter")}
        onChange={handleChange}
        value={values["password"]}
        error={!!errors["password"]}
        helperText={errors["password"]}
        type="password"
        required
      />
    </>
  );
};
