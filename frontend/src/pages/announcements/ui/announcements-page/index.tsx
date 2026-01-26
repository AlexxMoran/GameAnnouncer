import { CreateAnnouncementForm } from "@features/create-announcement/ui/create-announcement-form";
import AddIcon from "@mui/icons-material/Add";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { AnnouncementCard } from "@pages/announcements/ui/announcement-card";
import { MainPageImgStyled } from "@pages/announcements/ui/announcements-page/styles";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
} from "@shared/services/api/announcements-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import { CardsWrapperStyled } from "@shared/ui/_styled/cards-wrapper-styled";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { ElementObserver } from "@shared/ui/element-observer";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { useState, type FC, type RefObject } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { openDialog, closeDialog, confirm } = useDialog();
  const { enqueueSnackbar } = useSnackbar();
  const { announcementsApiService } = useRootService();

  const [announcementsService] = useState(
    () =>
      new EntityCrudService({
        getEntitiesFn: announcementsApiService.getAnnouncements,
        createEntityFn: announcementsApiService.createAnnouncement,
        deleteEntityFn: announcementsApiService.deleteAnnouncement,
      }),
  );

  const {
    paginationService,
    createEntity: createAnnouncement,
    deleteEntity: deleteAnnouncement,
  } = announcementsService;

  const { list, paginate, isInitialLoading, isPaginating, total } =
    paginationService;

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

  const createAnnouncementActionList = (
    announcement: IAnnouncementDto,
  ): IMenuAction[] => [
    {
      id: 1,
      title: t("actions.delete"),
      onClick: () => handleDeleteAnnouncement(announcement),
      icon: <DeleteOutlinedIcon />,
    },
  ];

  // TODO оптимизировать показ лоадера при пагинации
  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <MainPageImgStyled>
        <T
          variant="h5"
          sx={{
            position: "absolute",
            top: (theme) => theme.spacing(5),
            left: (theme) => theme.spacing(5),
            maxWidth: 500,
          }}
        >
          {t("texts.introduction")}
        </T>
      </MainPageImgStyled>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Badge nonce="" badgeContent={total} color="secondary">
          <T variant="h4">{t("pageTitles.announcements")}</T>
        </Badge>
        <Button
          variant="text"
          onClick={handleOpenCreateDialog}
          startIcon={<AddIcon />}
        >
          {t("actions.addAnnouncement")}
        </Button>
      </Box>
      {isInitialLoading && <Spinner type="backdrop" />}
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      {!!list.length && (
        <CardsWrapperStyled>
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
              <AnnouncementCard
                key={announcement.id}
                announcement={announcement}
                actionList={createAnnouncementActionList(announcement)}
              />
            ),
          )}
        </CardsWrapperStyled>
      )}
      {isPaginating && <Spinner type="pagination" />}
    </Box>
  );
});
