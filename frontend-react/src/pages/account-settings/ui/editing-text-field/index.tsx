import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import type { IEditingTextFieldProps } from "@pages/account-settings/ui/editing-text-field/types";
import { trimObjectValues } from "@shared/helpers/trimObjectValues";
import { TextField } from "@shared/ui/text-field";
import { useFormik } from "formik";
import type { ChangeEvent } from "react";
import { useState } from "react";
import { useDebounce } from "react-use";

// TODO подумать он выносе в единую логику (с одним инстансом formik)
export const EditingTextField = <TName extends string>(
  props: IEditingTextFieldProps<TName>
) => {
  const {
    onEdit,
    validationSchema,
    initialValues,
    ref: _,
    name,
    ...rest
  } = props;

  const formik = useFormik<Record<TName, string>>({
    onSubmit: async (values: Record<TName, string>) =>
      onEdit?.(trimObjectValues(values)),
    validationSchema,
    initialValues,
  });

  const [status, setStatus] = useState<"error" | "success" | undefined>();

  const { values, errors, isSubmitting, isValid } = formik;
  const { handleChange, submitForm } = formik;

  const handleInputChange = (event: ChangeEvent) => {
    setStatus(undefined);
    handleChange(event);
  };

  const handleBlur = () => {
    setStatus(undefined);
  };

  useDebounce(
    async () => {
      if (isValid && initialValues[name].trim() !== values[name].trim()) {
        try {
          await submitForm();

          setStatus("success");
        } catch (_) {
          setStatus("error");
        }
      }
    },
    300,
    [values[name]]
  );

  return (
    <TextField
      name={name}
      value={values[name]}
      helperText={errors[name] as string}
      error={status === "error" || !!errors[name]}
      color={status === "success" ? "success" : undefined}
      onChange={handleInputChange}
      onBlur={handleBlur}
      loading={isSubmitting}
      endAdornment={<EditOutlinedIcon fontSize="small" />}
      {...rest}
    />
  );
};
