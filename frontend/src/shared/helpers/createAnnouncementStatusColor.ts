import type { Theme } from "@mui/material";
import { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
// TODO вытащить в другое место
export const createAnnouncementStatusColor = (theme: Theme, status: EAnnouncementStatuses) => {
  const colors = {
    [EAnnouncementStatuses.PreRegistration]: theme.palette.warning.main,
    [EAnnouncementStatuses.RegistrationOpen]: theme.palette.success.main,
    [EAnnouncementStatuses.RegistrationClosed]: theme.palette.warning.main,
    [EAnnouncementStatuses.Live]: theme.palette.success.main,
    [EAnnouncementStatuses.Paused]: theme.palette.warning.main,
    [EAnnouncementStatuses.Finished]: theme.palette.background.paper,
    [EAnnouncementStatuses.Cancelled]: theme.palette.error.main,
  };

  return colors[status];
};
