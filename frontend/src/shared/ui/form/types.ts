import type { TObjectAny } from "@shared/types/main.types";
import type { IBoxProps } from "@shared/ui/box/types";
import type { FormikConfig } from "formik";
import type { FC } from "react";

export interface IFormikConfig<T extends TObjectAny> extends Omit<FormikConfig<T>, "onSubmit"> {
  onSubmit?: FormikConfig<T>["onSubmit"];
}

export interface IFormProps<TFormValues extends TObjectAny> {
  fields: FC;
  formikConfig: IFormikConfig<TFormValues>;
  onSubmit?: (values: TFormValues) => Promise<unknown> | void | undefined;
  onValidation?: (isValid: boolean) => void;
  onValuesChange?: (values: TFormValues) => void;
  buttonText?: string;
  wrapperStyles?: IBoxProps;
  cancelWithResult?: boolean;
  cancelButton?: {
    text: string;
    onCancel?: () => void;
  };
}
