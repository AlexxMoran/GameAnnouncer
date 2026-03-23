import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import type { IRegistrationRequestConfirmationProps } from "@pages/announcements/ui/registration-request-confirmation/types";
import { formatDate } from "@shared/lib/date/formatDate";
import { Box } from "@shared/ui/box";
import { Chip } from "@shared/ui/chip";
import { T } from "@shared/ui/typography";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationRequestConfirmation: FC<IRegistrationRequestConfirmationProps> = ({
  announcement,
  withForm,
}) => {
  const { title, game, start_at, participants_count, max_participants } = announcement;
  const { name } = game;

  const { t } = useTranslation();

  return (
    <Box maxWidth="450px" display="flex" flexDirection="column" gap={2}>
      <T variant="subtitle1">{title}</T>
      <Chip
        label={name}
        size="small"
        icon={<SportsEsportsIcon />}
        sx={{
          backgroundColor: (theme) => theme.palette.background.accent,
          alignSelf: "flex-start",
        }}
      />
      <Box
        sx={{
          p: 2,
          borderRadius: 2,
          backgroundColor: (theme) => theme.palette.background.accent,
          display: "flex",
          flexDirection: "column",
          gap: 1,
        }}
      >
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <T variant="body2" sx={{ color: "text.secondary" }}>
            {t("texts.startDate")}
          </T>
          <T variant="body2" sx={{ fontWeight: 600 }}>
            {formatDate(start_at)}
          </T>
        </Box>
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <T variant="body2" sx={{ color: "text.secondary" }}>
            {t("texts.participants")}
          </T>
          <T variant="body2" sx={{ fontWeight: 600 }}>
            {participants_count} / {max_participants}
          </T>
        </Box>
      </Box>
      <T variant="body2" sx={{ color: "text.secondary", lineHeight: 1.6 }}>
        {withForm ? t("texts.applyForTournamentFormMessage") : t("texts.applyForTournamentMessage")}
      </T>
    </Box>
  );
};
