import { useRootService } from "@shared/hooks/use-root-service";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import { useEffect, useState } from "react";

export const useAnnouncementsService = () => {
  const { announcementsApiService } = useRootService();

  const [announcementsService] = useState(
    () =>
      new EntityCrudService({
        getEntitiesFn: announcementsApiService.getAnnouncements,
        hasFiltersReaction: true,
      })
  );

  const { reactionList } = announcementsService;

  useEffect(() => () => reactionList.forEach((reaction) => reaction()), []);

  return announcementsService;
};
