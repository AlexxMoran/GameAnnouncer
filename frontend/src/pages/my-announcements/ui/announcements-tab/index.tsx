import { CreateAnnouncementForm } from "@features/create-announcement/ui/create-announcement-form";
import AddIcon from "@mui/icons-material/Add";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";

import { AnnouncementCard } from "@pages/my-announcements/ui/announcement-card";
import { EAppSubRoutes } from "@shared/constants/appRoutes";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IAnnouncementDto, ICreateAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { Divider } from "@shared/ui/divider";
import { ElementObserver } from "@shared/ui/element-observer";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { Fragment, useState, type FC, type RefObject } from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router";

export const AnnouncementsTab: FC = observer(() => {
  const location = useLocation();
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { openDialog, closeDialog, confirm } = useDialog();
  const { announcementsApiService } = useRootService();

  const tabType = location.pathname.split("/").at(-1) as
    | EAppSubRoutes.OrganizedAnnouncements
    | EAppSubRoutes.ParticipatedAnnouncements;

  const isParticipatedAnnouncements = tabType === EAppSubRoutes.ParticipatedAnnouncements;

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

  const {
    listData,
    createEntity: createAnnouncement,
    deleteEntity: deleteAnnouncement,
    paginate,
  } = announcementsService;

  const { list, isInitialLoading, isPaginating, total } = listData;

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
      title: t("actions.addAnnouncement"),
      children: <CreateAnnouncementForm onSubmit={handleCreateAnnouncement} />,
    });
  };

  const handleDeleteAnnouncement = async ({ id }: IAnnouncementDto) => {
    const result = await confirm({
      title: t("actions.deleteAnnouncement"),
      children: t("texts.deletionAnnouncementConfirmation"),
      confirmationText: t("actions.delete"),
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);
      const response = await deleteAnnouncement(id);

      if (response) {
        enqueueSnackbar(t("texts.announcementDeletingSuccess"), {
          variant: "success",
        });
        closeDialog();
      }
    }
  };

  const createAnnouncementActionList = (announcement: IAnnouncementDto): IMenuAction[] => [
    {
      id: 1,
      title: t("actions.delete"),
      onClick: () => handleDeleteAnnouncement(announcement),
      icon: <DeleteOutlinedIcon />,
    },
  ];

  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Badge badgeContent={total} color="secondary">
          <T variant="h6">
            {t(`texts.${isParticipatedAnnouncements ? "participatedAnnouncements" : "organizedAnnouncements"}`)}
          </T>
        </Badge>
        <Button variant="text" onClick={handleOpenCreateDialog} startIcon={<AddIcon />}>
          {t("actions.addAnnouncement")}
        </Button>
      </Box>
      {isInitialLoading && <Spinner type="backdrop" />}
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      {!!list.length && (
        <Box display="flex" flexDirection="column" gap={5}>
          {list.map((announcement, index) =>
            index === list.length - 1 ? (
              <ElementObserver key={announcement.id} onVisible={paginate}>
                {({ ref }) => (
                  <AnnouncementCard
                    ref={ref as RefObject<HTMLDivElement>}
                    announcement={announcement}
                    actionList={createAnnouncementActionList(announcement)}
                  />
                )}
              </ElementObserver>
            ) : (
              <Fragment key={announcement.id}>
                <AnnouncementCard announcement={announcement} actionList={createAnnouncementActionList(announcement)} />
                <Divider />
              </Fragment>
            )
          )}
        </Box>
      )}
      {isPaginating && <Spinner type="pagination" />}
    </Box>
  );
});
