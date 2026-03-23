import CancelIcon from "@mui/icons-material/Cancel";
import { createRequestStatusColor } from "@pages/registration-requests/model/create-request-status-color";
import type { IRequestCardProps } from "@pages/registration-requests/ui/request-card/types";
import { useDeviceType } from "@shared/hooks/use-device-type";
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
  const { isMobile, isDesktop } = useDeviceType();

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
      <Box
        display="flex"
        flexDirection="column"
        gap={2}
        flex={isMobile ? undefined : 1}
        width={isMobile ? "100%" : undefined}
        overflow="hidden"
      >
        <Box display="flex" alignItems="center" gap={1.5}>
          <T variant="subtitle2" color="textDisabled" sx={{ textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            № {id}
          </T>
          <T variant="subtitle2" sx={{ textOverflow: "ellipsis", whiteSpace: "nowrap", overflow: "hidden" }}>
            {title}
          </T>
          <Chip
            label={name}
            sx={{
              backgroundColor: (theme) => theme.palette.background.accent,
              ml: isMobile ? "auto" : undefined,
              maxWidth: !isDesktop ? "45%" : undefined,
            }}
          />
        </Box>
        <T variant="body2">{t("texts.submittedDate", { date: formatDate(created_at) })}</T>
      </Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" gap={2} flex={isMobile ? 1 : undefined}>
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
