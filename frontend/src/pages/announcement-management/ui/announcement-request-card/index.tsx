import { createRequestStatusColor } from "@entities/registration-request/lib/create-request-status-color";
import CancelIcon from "@mui/icons-material/Cancel";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { useTheme } from "@mui/material";
import type { IAnnouncementRequestCardProps } from "@pages/announcement-management/ui/announcement-request-card/types";
import { AVATAR_ICONS } from "@shared/constants/avatars";
import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";
import { Avatar } from "@shared/ui/avatar";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { IconButton } from "@shared/ui/icon-button";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementRequestCard: FC<IAnnouncementRequestCardProps> = observer(({ request }) => {
  const theme = useTheme();
  const { t } = useTranslation();

  const { status, user } = request;
  const { avatar_color, avatar_icon_id, nickname } = user;

  const isPending = request.status === ERegistrationRequestStatuses.Pending;

  const SelectedIcon =
    avatar_icon_id && AVATAR_ICONS[avatar_icon_id as keyof typeof AVATAR_ICONS]
      ? AVATAR_ICONS[avatar_icon_id as keyof typeof AVATAR_ICONS]
      : undefined;

  return (
    <Card
      sx={{
        padding: 2,
        backgroundColor: isPending ? theme.palette.background.info : undefined,
        borderColor: isPending ? theme.palette.secondary.dark : undefined,
      }}
    >
      <Box minHeight="80px" display="flex">
        <Box height="100%" display="flex" flexDirection="column" justifyContent="space-between" flex={1}>
          <Box display="flex" alignItems="center" gap={1}>
            <Avatar size={30} icon={SelectedIcon} color={avatar_color} username={nickname} />
            <T variant="body2">{nickname}</T>
          </Box>
          <Chip
            sx={{ alignSelf: "flex-start" }}
            label={t(`enums.registrationRequestStatuses.${status}`)}
            color={createRequestStatusColor(status)}
          />
        </Box>
        {isPending && (
          <Box height="100%" display="flex" flexDirection="column" justifyContent="space-between" gap={0.5}>
            <Tooltip title={t("actions.accept")} placement="left">
              <IconButton>
                <CheckCircleIcon color="success" fontSize="medium" />
              </IconButton>
            </Tooltip>
            <Tooltip title={t("actions.reject")} placement="left">
              <IconButton>
                <CancelIcon color="error" fontSize="medium" />
              </IconButton>
            </Tooltip>
          </Box>
        )}
      </Box>
    </Card>
  );
});
