import type { IRegistrationRequestFilters } from "@shared/services/api/registration-requests-api-service/types";

export interface IAnnouncementRequestFiltersProps {
  filters: Partial<IRegistrationRequestFilters>;
  handleFilter: (
    key: keyof IRegistrationRequestFilters,
    value: IRegistrationRequestFilters[keyof IRegistrationRequestFilters]
  ) => void;
}
