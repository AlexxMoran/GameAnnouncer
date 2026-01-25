import { createValidationSchema } from "@features/auth/model/create-validation-schema";
import { AuthFields } from "@features/auth/ui/auth-fields";
import type { IAuthFormProps } from "@features/auth/ui/auth-form/types";
import { Form } from "@shared/ui/form";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AuthForm: FC<IAuthFormProps> = (props) => {
  const { onSubmit, initialValues: values, buttonText } = props;

  const { t } = useTranslation();

  const initialValues = values || { username: "", password: "" };
  const validationSchema = createValidationSchema(t);

  return (
    <Form
      onSubmit={(values) => onSubmit?.(values)}
      formikConfig={{ initialValues, validationSchema }}
      fields={AuthFields}
      buttonText={buttonText}
    />
  );
};
