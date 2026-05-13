import type { IAnnouncementParticipantsCountInfoProps } from "@entities/announcement/ui/announcement-participants-count-info/types";
import PeopleIcon from "@mui/icons-material/People";
import { Box } from "@shared/ui/box";
import { LinearProgress } from "@shared/ui/linear-progress";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementParticipantsCountInfo: FC<IAnnouncementParticipantsCountInfoProps> = ({ announcement }) => {
  const { t } = useTranslation();

  const { participants_count = 0, max_participants = 0 } = announcement || {};

  const participantsInfo = `${participants_count} / ${max_participants}`;
  const participationPercent = max_participants > 0 ? (participants_count / max_participants) * 100 : 0;
  const progressColor = participationPercent >= 90 ? "error" : participationPercent >= 50 ? "warning" : "success";

  return (
    <div>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <PeopleIcon color="secondary" sx={{ fontSize: 16 }} />
          <T variant="caption" color="textSecondary">
            {t("texts.participants")}
          </T>
        </Box>
        <T variant="caption" color="textPrimary">
          <b>{participantsInfo}</b>
        </T>
      </Box>
      <LinearProgress variant="determinate" value={participationPercent} color={progressColor} />
    </div>
  );
};
