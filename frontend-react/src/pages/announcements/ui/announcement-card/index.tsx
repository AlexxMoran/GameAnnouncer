import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import PeopleIcon from "@mui/icons-material/People";
import { useTheme } from "@mui/material";
import { createAnnouncementStatusColor } from "@pages/announcements/ui/announcement-card/createAnnouncementStatusColor";
import type { IAnnouncementCardProps } from "@pages/announcements/ui/announcement-card/types";
import { CardLabelStyled } from "@shared/ui/_styled/card-label-styled";
import { EntityCardStyled } from "@shared/ui/_styled/entity-card-styled";
import { EntityImgStyled } from "@shared/ui/_styled/entity-img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { IconButton } from "@shared/ui/icon-button";
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
    <EntityCardStyled ref={ref}>
      <EntityImgStyled imgUrl={image_url}>
        <CardLabelStyled
          sx={{
            backgroundColor: (theme) => theme.palette.secondary.main,
            bottom: (theme) => theme.spacing(2),
            left: (theme) => theme.spacing(2),
            gap: (theme) => theme.spacing(2),
            display: "flex",
            alignItems: "center",
          }}
        >
          <PeopleIcon fontSize="small" />
          {participantsInfo}
        </CardLabelStyled>
        <CardLabelStyled
          sx={{
            backgroundColor: statusColor,
            top: (theme) => theme.spacing(2),
            left: (theme) => theme.spacing(2),
          }}
        >
          {t(`enums.announcementStatuses.${status}`)}
        </CardLabelStyled>
      </EntityImgStyled>
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
        <WithLineClampStyled variant="subtitle2">{title}</WithLineClampStyled>
        {content && (
          <WithLineClampStyled lineClamp={4} variant="caption">
            {content}
          </WithLineClampStyled>
        )}
      </Box>
    </EntityCardStyled>
  );
});
