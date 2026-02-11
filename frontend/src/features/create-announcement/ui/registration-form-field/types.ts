import type { ERegistrationFormFieldTypes } from "@shared/services/api/announcements-api-service/constants";
import type { IRegistrationFormField } from "@shared/services/api/announcements-api-service/types";
import type { TMaybe } from "@shared/types/main.types";
import type { FormikErrors } from "formik";
import type { ChangeEvent } from "react";

export interface IRegistrationFormFieldProps extends IRegistrationFormField {
  fieldKey: string;
  errors?: FormikErrors<Record<string, IRegistrationFormField>>;
  onChangeOption?: (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    fieldKey: string,
    optionKey: string
  ) => void;
  onDeleteOption?: (fieldKey: string, optionKey: string) => void;
  onAddOption?: (key: string) => void;
  onChangeType?: (value: TMaybe<ERegistrationFormFieldTypes>, key: string) => void;
  onChangeLabel?: (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>, key: string) => void;
  onDeleteField?: (key: string) => void;
  onChangeCheckbox?: (checked: boolean, key: string) => void;
}
