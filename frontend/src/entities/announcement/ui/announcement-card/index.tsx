import { createAnnouncementStatusColor } from "@entities/announcement/lib/create-announcement-status-color";
import type { IAnnouncementCardProps } from "@entities/announcement/ui/announcement-card/types";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import PeopleIcon from "@mui/icons-material/People";
import { useTheme } from "@mui/material";
import { formatDateRange } from "@shared/lib/formatDateRange";
import { ImgStyled } from "@shared/ui/_styled/img-styled";
import { WithLineClampStyled } from "@shared/ui/_styled/with-line-clamp-styled";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { LinearProgress } from "@shared/ui/linear-progress";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import { forwardRef } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementCard = forwardRef<HTMLDivElement, IAnnouncementCardProps>((props, ref) => {
  const { announcement, actionList, button } = props;

  const { t } = useTranslation();
  const theme = useTheme();

  const {
    image_url,
    title,
    content,
    participants_count,
    max_participants,
    status,
    registration_start_at,
    registration_end_at,
  } = announcement;

  const participantsInfo = `${participants_count} / ${max_participants}`;
  const participationPercent = max_participants > 0 ? (participants_count / max_participants) * 100 : 0;
  const statusColor = createAnnouncementStatusColor(theme, status);
  const progressColor = participationPercent >= 90 ? "error" : participationPercent >= 50 ? "warning" : "success";

  return (
    <Card
      ref={ref}
      sx={{
        height: "375px",
        cursor: "pointer",
        transition: "all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
        "&:hover": {
          borderColor: "primary.dark",
          transform: "translateY(-4px)",
          boxShadow: "0 12px 40px rgba(79, 195, 247, 0.12)",
        },
      }}
    >
      <ImgStyled imgUrl={image_url} sx={{ height: "35%" }}>
        <Chip
          label={t(`enums.announcementStatuses.${status}`)}
          size="small"
          sx={{
            position: "absolute",
            top: (theme) => theme.spacing(2),
            left: (theme) => theme.spacing(2),
            color: theme.palette.getContrastText(statusColor),
            backgroundColor: statusColor,
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
      <Box display="flex" flexDirection="column" justifyContent="space-between" flex={1} pb={3} pt={2} px={2}>
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
          <div>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <PeopleIcon color="secondary" sx={{ fontSize: 16 }} />
                <T variant="caption" color="textSecondary">
                  Участники
                </T>
              </Box>
              <T variant="caption" color="textPrimary">
                <b>{participantsInfo}</b>
              </T>
            </Box>
            <LinearProgress variant="determinate" value={participationPercent} color={progressColor} />
          </div>
        </Box>
        {button && (
          <Button onClick={button.onClick} startIcon={button.icon}>
            {button.title}
          </Button>
        )}
      </Box>
    </Card>
  );
});
