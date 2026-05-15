import type { IAnnouncementListFilters } from "@shared/services/api/announcements-api-service/types";

export interface IAnnouncementsFiltersProps {
  filters: Partial<IAnnouncementListFilters>;
  handleFilter: (
    key: keyof IAnnouncementListFilters,
    value: IAnnouncementListFilters[keyof IAnnouncementListFilters]
  ) => void;
}
