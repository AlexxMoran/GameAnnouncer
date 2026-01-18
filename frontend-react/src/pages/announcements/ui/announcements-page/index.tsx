import AddIcon from "@mui/icons-material/Add";
import { useTheme } from "@mui/material";
import { AnnouncementsService } from "@pages/announcements/model/announcements-service";
import { CreateAnnouncementForm } from "@pages/announcements/ui/create-announcement-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Fab } from "@shared/ui/fab-button";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { openDialog, closeDialog, confirm } = useDialog();
  const theme = useTheme();
  const { announcementsApiService } = useRootService();
  const [announcementsService] = useState(
    () => new AnnouncementsService(announcementsApiService)
  );

  const { paginationService, createGame } = announcementsService;
  const { list, paginate, isInitialLoading, isPaginating, total } =
    paginationService;

  const handleOpenCreateDialog = () => {
    openDialog({
      title: t("actions.addAnnouncement"),
      children: <CreateAnnouncementForm />,
    });
  };

  return (
    <Box display="flex" flexDirection="column" gap={8}>
      <Badge nonce="" badgeContent={total} color="secondary">
        <T variant="h4">{t("pageTitles.announcements")}</T>
      </Badge>
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      <Fab
        onClick={handleOpenCreateDialog}
        tooltip={t("actions.addAnnouncement")}
        sx={{
          position: "fixed",
          bottom: theme.spacing(6),
          right: theme.spacing(6),
        }}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
});
