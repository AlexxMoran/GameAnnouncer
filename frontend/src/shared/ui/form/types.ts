import type { TObjectAny } from "@shared/types/main.types";
import type { FormikConfig } from "formik";
import type { FC, PropsWithChildren } from "react";

export interface IFormikConfig<T extends TObjectAny> extends Omit<FormikConfig<T>, "onSubmit"> {
  onSubmit?: FormikConfig<T>["onSubmit"];
}

export interface IFormProps<TFormValues extends TObjectAny> extends PropsWithChildren {
  fields: FC;
  formikConfig: IFormikConfig<TFormValues>;
  onSubmit?: (values: TFormValues) => Promise<unknown> | void | undefined;
  onValidation?: (isValid: boolean) => void;
  onValuesChange?: (values: TFormValues) => void;
  onCancel?: () => void;
  confirmButtonText?: string;
  cancelButtonText?: string;
  cancelWithResult?: boolean;
  isForDialog?: boolean;
  disableOnSameValues?: boolean;
}
