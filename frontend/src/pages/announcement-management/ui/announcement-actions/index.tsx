import CancelIcon from "@mui/icons-material/Cancel";
import EditIcon from "@mui/icons-material/Edit";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { useCancelAnnouncement } from "@pages/announcement-management/model/use-cancel-announcement";
import { useEditAnnouncement } from "@pages/announcement-management/model/use-edit-announcement";
import { useStartAnnouncement } from "@pages/announcement-management/model/use-start-announcement";
import type { IAnnouncementActionsProps } from "@pages/announcement-management/ui/announcement-actions/types";
import { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementActions: FC<IAnnouncementActionsProps> = (props) => {
  const { announcement, cancelAnnouncement, startAnnouncement, editAnnouncement } = props;

  const { t } = useTranslation();
  const { handleCancelAnnouncement } = useCancelAnnouncement(cancelAnnouncement);
  const { handleStartAnnouncement } = useStartAnnouncement(startAnnouncement);
  const { handleOpenEditDialog } = useEditAnnouncement(editAnnouncement, announcement);

  const { status } = announcement || {};

  const actionList = (() => {
    const actionList = [];

    if (status !== EAnnouncementStatuses.Cancelled && status !== EAnnouncementStatuses.Finished) {
      if (status === EAnnouncementStatuses.RegistrationOpen) {
        actionList.push({
          title: t("actions.startTournament"),
          color: "primary" as const,
          onClick: handleStartAnnouncement,
          icon: <PlayArrowIcon />,
        });
      }

      if (status !== EAnnouncementStatuses.Live) {
        actionList.push({
          title: t("actions.edit"),
          color: "warning" as const,
          onClick: handleOpenEditDialog,
          icon: <EditIcon />,
        });
      }

      actionList.push({
        title: t("actions.cancelAnnouncement"),
        color: "error" as const,
        onClick: handleCancelAnnouncement,
        icon: <CancelIcon />,
      });
    }

    return actionList;
  })();

  if (!actionList.length) return null;

  return (
    <Card
      sx={{
        display: "flex",
        flexDirection: "column",
        padding: 3,
        gap: 2,
      }}
    >
      <T variant="h6" sx={{ "&::first-letter": { textTransform: "capitalize" } }}>
        {t("entities.action.many")}
      </T>
      <Box display="flex" flexDirection="column" gap={1.5}>
        {actionList.map(({ onClick, color, title, icon }) => (
          <Button key={title} onClick={onClick} color={color} startIcon={icon}>
            {title}
          </Button>
        ))}
      </Box>
    </Card>
  );
};
