import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import type { IRequestCardProps } from "@pages/my-announcements/ui/request-card/types";
import { useRootService } from "@shared/hooks/use-root-service";
import { formatDate } from "@shared/lib/formatDate";
import { ActionsMenu } from "@shared/ui/actions-menu";
import { Box } from "@shared/ui/box";
import { IconButton } from "@shared/ui/icon-button";
import { Spinner } from "@shared/ui/spinner";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import { forwardRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useAsync } from "react-use";

export const RequestCard = forwardRef<HTMLDivElement, IRequestCardProps>(({ request, actionList }) => {
  const { t } = useTranslation();
  const { announcementsApiService } = useRootService();
  const { gamesApiService } = useRootService();
  const [shouldFetch, setsShouldFetch] = useState(false);

  const { id, announcement_id, created_at, status } = request;

  const { loading, value: announcement } = useAsync(async () => {
    if (shouldFetch) {
      try {
        const {
          data: {
            data: { game_id, ...announcement },
          },
        } = await announcementsApiService.getAnnouncement(announcement_id);

        const {
          data: { data: game },
        } = await gamesApiService.getGame(game_id);

        return { ...announcement, game };
      } catch (_) {
        /* empty */
      }
    }
  }, [shouldFetch]);

  const announcementFieldList = [
    { label: t("entities.name"), value: announcement?.title },
    { label: t("entities.description"), value: announcement?.content || "-" },
    { label: t("entities.game"), value: announcement?.game?.name },
    { label: t("texts.announcementStartDate"), value: formatDate(announcement?.start_at) },
    {
      label: t("texts.registrationStartDate"),
      value: formatDate(announcement?.registration_start_at),
    },
    {
      label: t("texts.registrationEndDate"),
      value: formatDate(announcement?.registration_end_at),
    },
  ];

  const handleOpenTooltip = () => {
    setsShouldFetch(true);
  };

  return (
    <Box display="flex" gap={4} alignItems="center">
      <Tooltip
        placement="right"
        title={
          loading ? (
            <Spinner size={20} />
          ) : (
            <Box display="flex" gap={4} flexDirection="column">
              {announcementFieldList.map(({ label, value }) => (
                <Box display="flex" gap={2} key={label}>
                  <T variant="caption" sx={{ flex: 1 }} className="capitalize-first">
                    {label}
                  </T>
                  <T variant="caption" sx={{ flex: 1 }}>
                    {value}
                  </T>
                </Box>
              ))}
            </Box>
          )
        }
        hidden={!announcement || !loading}
        onOpen={handleOpenTooltip}
      >
        <HelpOutlineIcon sx={{ cursor: "pointer" }} />
      </Tooltip>
      <T sx={{ flex: 0.5 }}>
        № {id} | {formatDate(created_at)}
      </T>
      <T className="capitalize-first" sx={{ flex: 0.5 }}>
        {t("entities.status")}: {t(`enums.registrationRequestStatuses.${status}`)}
      </T>
      {actionList?.length && (
        <ActionsMenu actionList={actionList}>
          {({ onClick, ref }) => (
            <IconButton ref={ref} onClick={onClick}>
              <MoreHorizIcon />
            </IconButton>
          )}
        </ActionsMenu>
      )}
    </Box>
  );
});
