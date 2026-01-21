import type { ICreateAnnouncementDto } from "@shared/services/api/announcements-api-service/types";

export interface ICreateAnnouncementFormProps {
  onSubmit?: (values: ICreateAnnouncementDto) => Promise<unknown>;
}
