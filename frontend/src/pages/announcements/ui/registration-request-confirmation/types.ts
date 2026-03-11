import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";

export interface IRegistrationRequestConfirmationProps {
  announcement: IAnnouncementDto;
  withForm?: boolean;
}
