import type { IRegistrationFormField } from "@shared/services/api/announcements-api-service/types";

export interface IRegistrationFormFields {
  fields: Record<string, IRegistrationFormField>;
}

export interface IRegistrationFieldErrors {
  field_type: string;
  label: string;
  options: Record<string, string>;
}
