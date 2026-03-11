import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import type { ReactNode } from "react";

export interface IAnnouncementCardProps {
  announcement: IAnnouncementDto;
  actionList?: IMenuAction[];
  button?: {
    onClick: () => void;
    title: string;
    icon?: ReactNode;
  };
  height?: number;
}
