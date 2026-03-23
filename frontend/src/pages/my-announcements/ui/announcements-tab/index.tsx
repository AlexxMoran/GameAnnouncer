import { AnnouncementCard } from "@entities/announcement/ui/announcement-card";
import { CreateAnnouncementForm } from "@features/create-announcement/ui/create-announcement-form";
import AddIcon from "@mui/icons-material/Add";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import type { IAnnouncementsTabProps } from "@pages/my-announcements/ui/announcements-tab/types";
import { EMyAnnouncementsTabs } from "@shared/constants/appRoutes";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IAnnouncementDto, ICreateAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { useCallback, useState, type FC } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router";

export const AnnouncementsTab: FC<IAnnouncementsTabProps> = observer(({ canAddAnnouncements }) => {
  const location = useLocation();
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog } = useDialog();
  const { announcementsApiService } = useRootService();

  const tabType = location.pathname.split("/").at(-1) as EMyAnnouncementsTabs;

  const isParticipatedAnnouncements = tabType === EMyAnnouncementsTabs.Participated;

  const [announcementsService] = useState(
    () =>
      new EntityCrudService({
        getEntitiesFn:
          announcementsApiService[
            isParticipatedAnnouncements ? "getParticipatedAnnouncements" : "getOrganizedAnnouncements"
          ],
        createEntityFn: announcementsApiService.createAnnouncement,
        deleteEntityFn: announcementsApiService.deleteAnnouncement,
      })
  );

  const { listData, createEntity: createAnnouncement, paginate } = announcementsService;

  const subtitle =
    tabType === EMyAnnouncementsTabs.Organized
      ? t("texts.tournamentsCreatedAndOrganize")
      : t("texts.tournamentsParticipated");

  const noDataSubtitle =
    tabType === EMyAnnouncementsTabs.Organized
      ? t("texts.howToCreateTournament")
      : t("texts.howToParticipateInTournament");

  const handleCreateAnnouncement = async (values: ICreateAnnouncementDto) => {
    const result = await createAnnouncement(values);

    if (result) {
      enqueueSnackbar(t("texts.announcementAddingSuccess"), {
        variant: "success",
      });
      closeDialog();
    }
  };

  const handleOpenCreateDialog = () => {
    openDialog({
      title: t("actions.createTournament"),
      children: <CreateAnnouncementForm onSubmit={handleCreateAnnouncement} />,
    });
  };

  const renderItem = useCallback(
    (announcement: IAnnouncementDto) => (
      <AnnouncementCard height={275} key={announcement.id} announcement={announcement} />
    ),
    [t]
  );

  return (
    <Box display="flex" flexDirection="column" gap={3} height="100%">
      <Box display="flex" flexDirection="column" gap={1}>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Badge badgeContent={listData.filteredCount} color="secondary">
            <T variant="h5" sx={{ "&::first-letter": { textTransform: "capitalize" } }}>
              {t("entities.announcement.many")}
            </T>
          </Badge>
          {canAddAnnouncements && (
            <Button variant="text" onClick={handleOpenCreateDialog} startIcon={<AddIcon />}>
              {t("actions.createTournament")}
            </Button>
          )}
        </Box>
        <T variant="body2" color="textSecondary">
          {subtitle}
        </T>
      </Box>
      <InfiniteScrollList
        renderItem={renderItem}
        onLoadMore={paginate}
        noDataIcon={EmojiEventsIcon}
        noDataTitle={t("texts.noTournaments")}
        noDataSubtitle={noDataSubtitle}
        {...listData}
      />
    </Box>
  );
});
