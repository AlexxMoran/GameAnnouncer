import { createAnnouncementStatusColor } from "@entities/announcement/lib/create-announcement-status-color";
import type { IAnnouncementCardProps } from "@entities/announcement/ui/announcement-card/types";
import { AnnouncementParticipantsCountInfo } from "@entities/announcement/ui/announcement-participants-count-info";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import { useTheme } from "@mui/material";
import { formatDateRange } from "@shared/lib/date/formatDateRange";
import { ImgStyled } from "@shared/ui/_styled/img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import { type FC, type MouseEvent } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementCard: FC<IAnnouncementCardProps> = (props) => {
  const { announcement, actionList, button } = props;

  const { t } = useTranslation();
  const theme = useTheme();

  const { game, title, content, status, registration_start_at, registration_end_at } = announcement;
  const { image_url, name } = game;

  const statusColor = createAnnouncementStatusColor(theme, status);

  const handleButtonClick = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    button?.onClick();
  };

  return (
    <Card
      sx={{
        height: "380px",
        cursor: "pointer",
        transition: "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        "@media (hover: hover) and (pointer: fine)": {
          "&:hover": {
            borderColor: "primary.dark",
            transform: "translateY(-4px)",
            boxShadow: "0 12px 40px rgba(79, 195, 247, 0.12)",
          },
        },
      }}
    >
      <ImgStyled imgUrl={image_url} sx={{ height: "140px" }}>
        <Chip
          label={t(`enums.announcementStatuses.${status}`)}
          sx={{
            position: "absolute",
            top: (theme) => theme.spacing(1.5),
            left: (theme) => theme.spacing(1.5),
            color: (theme) => theme.palette.getContrastText(statusColor),
            backgroundColor: statusColor,
          }}
        />
        <Chip
          icon={<SportsEsportsIcon />}
          label={name}
          sx={{
            position: "absolute",
            top: (theme) => theme.spacing(1.5),
            right: (theme) => theme.spacing(1.5),
            backgroundColor: (theme) => theme.palette.background.accent,
            width: "40%",
            maxWidth: "200px",
          }}
        />
        {actionList?.length && (
          <Box position="absolute" bottom={8} right={8} display="flex" gap={0.5}>
            {actionList.map(({ icon, id, onClick, title, color }) => (
              <Tooltip title={title}>
                <IconButton key={id} onClick={() => onClick?.()} color={color}>
                  {icon}
                </IconButton>
              </Tooltip>
            ))}
          </Box>
        )}
      </ImgStyled>
      <Box display="flex" flexDirection="column" gap={2.5} flex={1} pb={3} pt={1.5} px={2}>
        <Box display="flex" flexDirection="column" gap={0.5}>
          <WithLineClampStyled lineClamp={1} variant="h6">
            {title}
          </WithLineClampStyled>
          {content && (
            <WithLineClampStyled lineClamp={2} variant="body2" color="textSecondary">
              {content}
            </WithLineClampStyled>
          )}
        </Box>
        <Box display="flex" flexDirection="column" gap={0.5}>
          <Box display="flex" gap={1}>
            <CalendarTodayIcon color="primary" sx={{ fontSize: 16 }} />
            <T variant="caption" color="textSecondary">
              {formatDateRange(registration_start_at, registration_end_at)}
            </T>
          </Box>
          <AnnouncementParticipantsCountInfo announcement={announcement} />
        </Box>
        {button && (
          <Button sx={{ marginTop: "auto" }} onClick={handleButtonClick} startIcon={button.icon}>
            {button.title}
          </Button>
        )}
      </Box>
    </Card>
  );
};
