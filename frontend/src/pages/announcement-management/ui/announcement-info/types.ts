import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { TMaybe } from "@shared/types/main.types";

export interface IAnnouncementInfoProps {
  announcement: TMaybe<IAnnouncementDto>;
}
