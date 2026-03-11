import type {
  IAnnouncementDto,
  IRegistrationFormFieldWithId,
} from "@shared/services/api/announcements-api-service/types";

export interface IRegistrationRequestFormProps {
  fieldList: IRegistrationFormFieldWithId[];
  announcement: IAnnouncementDto;
  onSubmit?: (values: Record<string, string | boolean>) => Promise<void>;
}
