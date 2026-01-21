import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import PeopleIcon from "@mui/icons-material/People";
import { useTheme } from "@mui/material";
import { createAnnouncementStatusColor } from "@pages/announcements/ui/announcement-card/createAnnouncementStatusColor";
import {
  AnnouncementCardWrapperStyled,
  AnnouncementDescriptionStyled,
  AnnouncementImgStyled,
  AnnouncementStatusStyled,
  ParticipantsCountStyled,
} from "@pages/announcements/ui/announcement-card/styles";
import type { IAnnouncementCardProps } from "@pages/announcements/ui/announcement-card/types";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { IconButton } from "@shared/ui/icon-button";
import { T } from "@shared/ui/typography";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementCard = forwardRef<
  HTMLDivElement,
  IAnnouncementCardProps
>((props, ref) => {
  const { announcement, actionList } = props;

  const { t } = useTranslation();
  const theme = useTheme();

  const {
    image_url,
    title,
    content,
    participants_count,
    max_participants,
    status,
  } = announcement;

  const participantsInfo = `${participants_count} / ${max_participants}`;
  const statusColor = createAnnouncementStatusColor(theme, status);

  return (
    <AnnouncementCardWrapperStyled ref={ref}>
      <AnnouncementImgStyled imgUrl={image_url}>
        <ParticipantsCountStyled>
          <PeopleIcon />
          {participantsInfo}
        </ParticipantsCountStyled>
        <AnnouncementStatusStyled sx={{ backgroundColor: statusColor }}>
          {t(`enums.announcementStatuses.${status}`)}
        </AnnouncementStatusStyled>
      </AnnouncementImgStyled>
      {actionList?.length && (
        <Box position="absolute" top={8} right={8}>
          <ActionsMenu actionList={actionList}>
            {({ onClick, ref }) => (
              <IconButton ref={ref} onClick={onClick}>
                <MoreHorizIcon />
              </IconButton>
            )}
          </ActionsMenu>
        </Box>
      )}
      <Box display="flex" flexDirection="column" gap={2} flex={1} p={3}>
        <T variant="h6">{title}</T>
        {content && (
          <AnnouncementDescriptionStyled variant="body1">
            {content}
          </AnnouncementDescriptionStyled>
        )}
        <Button sx={{ mt: "auto" }}>{t("actions.viewAnnouncement")}</Button>
      </Box>
    </AnnouncementCardWrapperStyled>
  );
});
