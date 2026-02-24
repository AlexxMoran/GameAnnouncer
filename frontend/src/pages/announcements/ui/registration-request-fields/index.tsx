import type { IRegistrationRequestFieldsProps } from "@pages/announcements/ui/registration-request-fields/types";
import { ERegistrationFormFieldTypes } from "@shared/services/api/announcements-api-service/constants";
import type { TMaybe } from "@shared/types/main.types";
import { Autocomplete } from "@shared/ui/autocomplete";
import { FormControlLabel } from "@shared/ui/form-control-label";
import { Switch } from "@shared/ui/switch";
import { TextField } from "@shared/ui/text-field";
import { useFormikContext } from "formik";
import type { FC } from "react";

export const RegistrationRequestFields: FC<IRegistrationRequestFieldsProps> = ({ fieldList }) => {
  const { errors, values, handleChange, setFieldValue } = useFormikContext<Record<string, string | boolean>>();

  const handleChangeSelect = (name: string, value: TMaybe<string>) => {
    setFieldValue(name, value);
  };

  const handleSwitchChange = (name: string, checked: boolean) => {
    setFieldValue(name, checked);
  };

  return (
    <>
      {fieldList.map(({ field_type, label, id, options }) => {
        const name = id.toString();

        if (field_type === ERegistrationFormFieldTypes.Text) {
          return (
            <TextField
              key={id}
              name={name}
              label={label}
              onChange={handleChange}
              value={values[name]}
              error={!!errors[name]}
              helperText={errors[name]}
              required
            />
          );
        }

        if (field_type === ERegistrationFormFieldTypes.Select && options) {
          return (
            <Autocomplete
              key={id}
              name={name}
              label={label}
              onChange={(_, value) => handleChangeSelect(name, value)}
              value={values[name]?.toString()}
              error={!!errors[name]}
              helperText={errors[name]}
              options={options}
              required
            />
          );
        }

        if (field_type === ERegistrationFormFieldTypes.Boolean) {
          return (
            <FormControlLabel
              key={id}
              name="has_qualification"
              label={label}
              control={<Switch checked={!!values[name]} />}
              onChange={(_, value) => handleSwitchChange(name, value)}
            />
          );
        }
      })}
    </>
  );
};
