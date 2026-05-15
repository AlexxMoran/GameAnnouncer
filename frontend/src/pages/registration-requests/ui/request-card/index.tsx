import { createRequestStatusColor } from "@entities/registration-request/lib/create-request-status-color";
import CancelIcon from "@mui/icons-material/Cancel";
import type { IRequestCardProps } from "@pages/registration-requests/ui/request-card/types";
import { formatDate } from "@shared/lib/date/formatDate";
import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { T } from "@shared/ui/typography";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const RequestCard: FC<IRequestCardProps> = ({ request, onCancelRequest }) => {
  const { t } = useTranslation();

  const { id, announcement, created_at, status } = request;
  const { game, title } = announcement;
  const { name } = game;

  const showCancelButton =
    status === ERegistrationRequestStatuses.Approved || status === ERegistrationRequestStatuses.Pending;

  return (
    <Card
      sx={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        flexWrap: "wrap",
        padding: 2,
        gap: 2,
      }}
    >
      <Box display="flex" flexDirection="column" gap={2} width={"100%"} overflow="hidden">
        <Box display="flex" alignItems="center" gap={1.5}>
          <T variant="subtitle2" color="textSecondary" sx={{ textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            № {id}
          </T>
          <T variant="subtitle2" sx={{ textOverflow: "ellipsis", whiteSpace: "nowrap", overflow: "hidden" }}>
            {title}
          </T>
          <Chip
            label={name}
            sx={{
              backgroundColor: (theme) => theme.palette.background.accent,
              ml: "auto",
              maxWidth: "45%",
            }}
          />
        </Box>
        <T variant="body2">{t("texts.submittedDate", { date: formatDate(created_at) })}</T>
      </Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" gap={2} flex={1}>
        <Chip label={t(`enums.registrationRequestStatuses.${status}`)} color={createRequestStatusColor(status)} />
        {showCancelButton && (
          <Button variant="text" color="error" startIcon={<CancelIcon />} onClick={onCancelRequest}>
            {t("actions.cancel")}
          </Button>
        )}
      </Box>
    </Card>
  );
};
