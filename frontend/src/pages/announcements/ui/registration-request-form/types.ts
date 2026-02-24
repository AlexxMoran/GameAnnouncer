import type { IRegistrationFormFieldWithId } from "@shared/services/api/announcements-api-service/types";

export interface IRegistrationRequestFormProps {
  fieldList: IRegistrationFormFieldWithId[];
  onSubmit?: (values: Record<string, string | boolean>) => Promise<void>;
}
