import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";

export interface IAnnouncementCardProps {
  announcement: IAnnouncementDto;
  actionList?: IMenuAction[];
}

export interface IGameImgStyledProps {
  imgUrl?: string;
}
