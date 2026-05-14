import type { IAnnouncementDto, ICreateAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { TMaybe } from "@shared/types/main.types";

export interface ICreateAnnouncementFormProps {
  onSubmit?: (values: ICreateAnnouncementDto) => Promise<unknown>;
  announcement?: TMaybe<IAnnouncementDto>;
}
