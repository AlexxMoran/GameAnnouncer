import type { IAnnouncementRequestFiltersProps } from "@pages/announcement-management/ui/announcement-request-filters/types";
import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";
import { Box } from "@shared/ui/box";
import { Chip } from "@shared/ui/chip";
import { observer } from "mobx-react-lite";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementRequestFilters: FC<IAnnouncementRequestFiltersProps> = observer((props) => {
  const { filters, handleFilter } = props;

  const { t } = useTranslation();

  const handleSetStatus = (status: ERegistrationRequestStatuses) => {
    if (filters.status === status) {
      handleFilter("status", undefined);
    } else {
      handleFilter("status", status);
    }
  };

  return (
    <Box display="flex" gap={1} width="100%" flexWrap="wrap">
      {Object.values(ERegistrationRequestStatuses).map((status) => (
        <Chip
          key={status}
          size="medium"
          label={t(`enums.registrationRequestStatuses.${status}`)}
          variant={filters.status === status ? "filled" : "outlined"}
          onClick={() => handleSetStatus(status)}
        />
      ))}
    </Box>
  );
});
