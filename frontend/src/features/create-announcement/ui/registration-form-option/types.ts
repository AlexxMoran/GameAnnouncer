import type { ChangeEvent } from "react";

export interface IRegistrationFormOptionProps {
  fieldKey: string;
  optionKey: string;
  isDeletionDisabled: boolean;
  optionValue: string;
  error?: string;
  onChangeOption?: (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    fieldKey: string,
    optionKey: string
  ) => void;
  onDeleteOption?: (fieldKey: string, optionKey: string) => void;
}
