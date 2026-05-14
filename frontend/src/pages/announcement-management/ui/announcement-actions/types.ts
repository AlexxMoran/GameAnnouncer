import type { IAnnouncementDto, IEditAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type { TMaybe } from "@shared/types/main.types";

export interface IAnnouncementActionsProps {
  announcement: TMaybe<IAnnouncementDto>;
  cancelAnnouncement: () => Promise<TApiResponseWrapper<IAnnouncementDto> | undefined>;
  startAnnouncement: () => Promise<TApiResponseWrapper<IAnnouncementDto> | undefined>;
  editAnnouncement: (params: IEditAnnouncementDto) => Promise<TApiResponseWrapper<IAnnouncementDto> | undefined>;
}
