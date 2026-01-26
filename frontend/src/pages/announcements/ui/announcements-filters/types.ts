import type { IGetAnnouncementsDto } from "@shared/services/api/announcements-api-service/types";

export interface IAnnouncementsFiltersProps {
  filters: Partial<IGetAnnouncementsDto>;
  handleFilter: (
    key: keyof IGetAnnouncementsDto,
    value: IGetAnnouncementsDto[keyof IGetAnnouncementsDto],
  ) => void;
}
