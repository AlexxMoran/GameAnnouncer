import ClearIcon from "@mui/icons-material/Clear";
import SearchIcon from "@mui/icons-material/Search";
import type { IAnnouncementsFiltersProps } from "@pages/announcements/ui/announcements-filters/types";
import { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
import { Box } from "@shared/ui/box";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { TextField } from "@shared/ui/text-field";
import { observer } from "mobx-react-lite";
import { type ChangeEvent, type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsFilters: FC<IAnnouncementsFiltersProps> = observer((props) => {
  const { filters, handleFilter } = props;

  const { t } = useTranslation();

  const handleSearchInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    handleFilter("q", event.target.value);
  };

  const handleClearSearchInput = () => {
    handleFilter("q", undefined);
  };

  const handleSetStatus = (status: EAnnouncementStatuses) => {
    if (filters.status === status) {
      handleFilter("status", undefined);
    } else {
      handleFilter("status", status);
    }
  };

  return (
    <>
      <TextField
        value={filters["q"] || ""}
        endAdornment={
          <>
            {filters["q"] && (
              <IconButton onClick={handleClearSearchInput} edge="end" size="small">
                <ClearIcon />
              </IconButton>
            )}
            <SearchIcon />
          </>
        }
        placeholder={t("placeholders.search")}
        onChange={handleSearchInputChange}
      />
      <Box display="flex" gap={1} width="100%" flexWrap="wrap">
        {[
          EAnnouncementStatuses.Live,
          EAnnouncementStatuses.RegistrationOpen,
          EAnnouncementStatuses.PreRegistration,
          EAnnouncementStatuses.Cancelled,
        ].map((status) => (
          <Chip
            key={status}
            size="small"
            label={t(`enums.announcementStatuses.${status}`)}
            variant={filters.status === status ? "filled" : "outlined"}
            onClick={() => handleSetStatus(status)}
          />
        ))}
      </Box>
    </>
  );
});
