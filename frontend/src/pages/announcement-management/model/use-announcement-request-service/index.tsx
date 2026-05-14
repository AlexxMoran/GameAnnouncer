import { AnnouncementRequestsService } from "@pages/announcement-management/model/announcement-requests-service";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import { useEffect, useState } from "react";

export const useAnnouncementRequestsService = (announcement: IAnnouncementDto) => {
  const { registrationRequestsApiService } = useRootService();

  const [announcementRequestsService] = useState(
    () => new AnnouncementRequestsService(registrationRequestsApiService, announcement.id)
  );

  const { reactionList } = announcementRequestsService;

  useEffect(() => () => reactionList.forEach((reaction) => reaction()), []);

  return announcementRequestsService;
};
