import type { ITextFieldProps } from "@shared/ui/text-field/types";
import type { FormikConfig } from "formik";

export interface IEditingTextFieldProps<TName extends string>
  extends ITextFieldProps {
  name: TName;
  initialValues: Record<TName, string>;
  validationSchema?: FormikConfig<Record<TName, string>>["validationSchema"];
  onEdit?: (params: Record<TName, string>) => Promise<void> | undefined | void;
}
