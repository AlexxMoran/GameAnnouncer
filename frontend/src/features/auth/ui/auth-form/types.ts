import type { IAuthFields } from "@features/auth/model/create-validation-schema/types";

export interface IAuthFormProps {
  onSubmit?: (values: IAuthFields) => Promise<unknown>;
  initialValues?: IAuthFields;
  buttonText?: string;
}
