import AddIcon from "@mui/icons-material/Add";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import { useTheme } from "@mui/material";
import { AnnouncementsService } from "@pages/announcements/model/announcements-service";
import { AnnouncementCard } from "@pages/announcements/ui/announcement-card";
import { MainPageImgStyled } from "@pages/announcements/ui/announcements-page/styles";
import { CreateAnnouncementForm } from "@pages/announcements/ui/create-announcement-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
} from "@shared/services/api/announcements-api-service/types";
import { CardsWrapperStyled } from "@shared/ui/_styled/cards-wrapper-styled";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { ElementObserver } from "@shared/ui/element-observer";
import { Fab } from "@shared/ui/fab-button";
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
  const theme = useTheme();
  const { announcementsApiService } = useRootService();

  const [announcementsService] = useState(
    () => new AnnouncementsService(announcementsApiService)
  );

  const { paginationService, createAnnouncement, deleteAnnouncement } =
    announcementsService;

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
    announcement: IAnnouncementDto
  ): IMenuAction[] => [
    {
      id: 3,
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
      <Badge nonce="" badgeContent={total} color="secondary">
        <T variant="h4">{t("pageTitles.announcements")}</T>
      </Badge>
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
            )
          )}
        </CardsWrapperStyled>
      )}
      {isPaginating && <Spinner type="pagination" />}
      <Fab
        onClick={handleOpenCreateDialog}
        tooltip={t("actions.addAnnouncement")}
        sx={{
          position: "fixed",
          bottom: theme.spacing(6),
          right: theme.spacing(6),
        }}
      >
        <AddIcon />
      </Fab>
    </Box>
  );
});
