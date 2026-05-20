import { createRequestStatusColor } from "@entities/registration-request/lib/create-request-status-color";
import CancelIcon from "@mui/icons-material/Cancel";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import { useTheme } from "@mui/material";
import { useApproveRequest } from "@pages/announcement-management/model/use-approve-request";
import { useCancelRequestRequest } from "@pages/announcement-management/model/use-cancel-request";
import type { IAnnouncementRequestCardProps } from "@pages/announcement-management/ui/announcement-request-card/types";
import { AVATAR_ICONS } from "@shared/constants/avatars";
import { useDeviceType } from "@shared/hooks/use-device-type";
import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";
import { Avatar } from "@shared/ui/avatar";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Card } from "@shared/ui/card";
import { Chip } from "@shared/ui/chip";
import { Collapse } from "@shared/ui/collapse";
import { Divider } from "@shared/ui/divider";
import { IconButton } from "@shared/ui/icon-button";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import isEmpty from "lodash/isEmpty";
import { observer } from "mobx-react-lite";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementRequestCard: FC<IAnnouncementRequestCardProps> = observer((props) => {
  const { request, changeRequestStatus } = props;

  const theme = useTheme();
  const { t } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);
  const { isMobile } = useDeviceType();

  const { handleOpenRequestCancellationDialog } = useCancelRequestRequest(request, (params) =>
    changeRequestStatus(request.id, params)
  );

  const { handleApproveRequest } = useApproveRequest(request, (params) => changeRequestStatus(request.id, params));

  const { status, user, form_responses } = request;
  const { avatar_color, avatar_icon_id, nickname } = user;

  const isPending = request.status === ERegistrationRequestStatuses.Pending;
  const showDetails = !!form_responses && !isEmpty(form_responses);

  const SelectedIcon =
    avatar_icon_id && AVATAR_ICONS[avatar_icon_id as keyof typeof AVATAR_ICONS]
      ? AVATAR_ICONS[avatar_icon_id as keyof typeof AVATAR_ICONS]
      : undefined;

  const handleToggleDetails = () => {
    setIsExpanded((state) => !state);
  };

  return (
    <Card
      sx={{
        padding: 1.5,
        backgroundColor: isPending ? theme.palette.background.info : undefined,
        borderColor: isPending ? theme.palette.secondary.dark : undefined,
      }}
    >
      <Box display="flex" flexDirection="column" gap={1.5}>
        <Box display="flex" alignItems="center" justifyContent="space-between" gap={0.5}>
          <Box display="flex" alignItems="center" gap={1} minWidth={0}>
            <Avatar size={30} icon={SelectedIcon} color={avatar_color} username={nickname} />
            <T
              sx={{
                flex: 1,
                minWidth: 0,
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
                overflow: "hidden",
              }}
              variant="body2"
            >
              {nickname}
            </T>
          </Box>
          <Box display="flex" alignItems="center" justifyContent="space-between" gap={1.5}>
            <Chip label={t(`enums.registrationRequestStatuses.${status}`)} color={createRequestStatusColor(status)} />
            {!isMobile && (
              <>
                {isPending && (
                  <Box height="100%" display="flex" gap={0.5}>
                    <Tooltip title={t("actions.reject")}>
                      <IconButton size="medium" onClick={handleOpenRequestCancellationDialog}>
                        <CancelIcon color="error" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title={t("actions.accept")}>
                      <IconButton size="medium" onClick={handleApproveRequest}>
                        <CheckCircleIcon color="success" />
                      </IconButton>
                    </Tooltip>
                  </Box>
                )}
                {showDetails && (
                  <Tooltip title={t(`actions.${isExpanded ? "hideDetails" : "viewDetails"}`)}>
                    <IconButton
                      size="medium"
                      sx={{ transform: isExpanded ? "rotate(180deg)" : "rotate(0deg)" }}
                      onClick={handleToggleDetails}
                    >
                      <KeyboardArrowDownIcon />
                    </IconButton>
                  </Tooltip>
                )}
              </>
            )}
          </Box>
        </Box>
        {isMobile && (showDetails || isPending) && (
          <Box display="flex" justifyContent="space-between">
            {showDetails && (
              <Button
                endIcon={<KeyboardArrowDownIcon sx={{ transform: isExpanded ? "rotate(180deg)" : "rotate(0deg)" }} />}
                size="small"
                onClick={handleToggleDetails}
                variant="outlined"
                fullWidth={!isPending}
              >
                {t(`texts.details`)}
              </Button>
            )}
            {isPending && (
              <Box height="100%" display="flex" gap={0.5} ml="auto">
                <Button size="small" color="error" onClick={handleOpenRequestCancellationDialog}>
                  {t("actions.reject")}
                </Button>
                <Button size="small" color="success" onClick={handleApproveRequest}>
                  {t("actions.accept")}
                </Button>
              </Box>
            )}
          </Box>
        )}
      </Box>
      {showDetails && (
        <Collapse in={isExpanded}>
          <Box pt={1.5} display="flex" flexDirection="column" gap={1.5}>
            <Divider />
            <Box display="flex" flexDirection="column" gap={1}>
              {form_responses.map(({ value, label, form_field_id }) => (
                <Box display="flex" flexDirection="column" key={form_field_id}>
                  <T color="textSecondary" sx={{ textTransform: "uppercase" }} variant="caption">
                    {label}
                  </T>
                  <T variant="subtitle2">{value || "-"}</T>
                </Box>
              ))}
            </Box>
          </Box>
        </Collapse>
      )}
    </Card>
  );
});
