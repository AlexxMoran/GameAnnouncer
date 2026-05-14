import { AnnouncementParticipantsCountInfo } from "@entities/announcement/ui/announcement-participants-count-info";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import InsertInvitationIcon from "@mui/icons-material/InsertInvitation";
import type { IAnnouncementInfoProps } from "@pages/announcement-management/ui/announcement-info/types";
import { formatDate } from "@shared/lib/date/formatDate";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { Divider } from "@shared/ui/divider";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementInfo: FC<IAnnouncementInfoProps> = observer(({ announcement }) => {
  const { t } = useTranslation();

  const { content, registration_end_at, registration_start_at, start_at, end_at } = announcement || {};

  const dateList = [
    {
      label: t("texts.registrationStartDate"),
      date: registration_start_at,
      Icon: CalendarTodayIcon,
      iconColor: "primary" as const,
    },
    {
      label: t("texts.registrationEndDate"),
      date: registration_end_at,
      Icon: InsertInvitationIcon,
      iconColor: "primary" as const,
    },
    { label: t("texts.announcementStartDate"), date: start_at, Icon: CalendarTodayIcon, iconColor: "success" as const },
    { label: t("texts.announcementEndDate"), date: end_at, Icon: InsertInvitationIcon, iconColor: "error" as const },
  ];

  return (
    <Card
      sx={{
        display: "flex",
        flexDirection: "column",
        padding: { xs: 2, sm: 3 },
        gap: 2,
      }}
    >
      <T variant="h6" sx={{ "&::first-letter": { textTransform: "capitalize" } }}>
        {t("texts.announcementInfo")}
      </T>
      <Box display="flex" flexDirection="column" gap={1.5}>
        {content && (
          <>
            <T variant="body2" color="textSecondary">
              {content}
            </T>
            <Divider />
          </>
        )}
        {dateList.map(
          ({ date, iconColor, Icon, label }) =>
            date && (
              <Box display="flex" alignItems="center" gap={1.5} key={label}>
                <Icon color={iconColor} />
                <Box display="flex" flexDirection="column">
                  <T color="textSecondary" variant="caption">
                    {label}
                  </T>
                  <T variant="subtitle2">{formatDate(date)}</T>
                </Box>
              </Box>
            )
        )}
        <Divider />
        <AnnouncementParticipantsCountInfo announcement={announcement} />
      </Box>
    </Card>
  );
});
