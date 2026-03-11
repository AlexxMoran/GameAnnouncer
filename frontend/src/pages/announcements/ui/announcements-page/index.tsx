import { AnnouncementCard } from "@entities/announcement/ui/announcement-card";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";
import { useTheme } from "@mui/material";
import { AnnouncementsFilters } from "@pages/announcements/ui/announcements-filters";
import { MainPageImgContentStyled, MainPageImgStyled } from "@pages/announcements/ui/announcements-page/styles";
import { RegistrationRequestForm } from "@pages/announcements/ui/registration-request-form";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { ICreateRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import { PageWrapperStyled } from "@shared/ui/_styled/page-wrapper-styled";
import { Badge } from "@shared/ui/badge";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { T } from "@shared/ui/typography";
import { isEmpty } from "lodash";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { useEffect, useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { openDialog, closeDialog, confirm } = useDialog();
  const { enqueueSnackbar } = useSnackbar();
  const theme = useTheme();
  const { announcementsApiService, registrationRequestsApiService } = useRootService();

  const [announcementsService] = useState(
    () =>
      new EntityCrudService({
        getEntitiesFn: announcementsApiService.getAnnouncements,
        createEntityFn: announcementsApiService.createAnnouncement,
        deleteEntityFn: announcementsApiService.deleteAnnouncement,
        hasFiltersReaction: true,
      })
  );

  const { listData, reactionList, filters, setFilter, paginate } = announcementsService;
  const { createRegistrationRequest } = registrationRequestsApiService;

  // const handleDeleteAnnouncement = async ({ id }: IAnnouncementDto) => {
  //   const result = await confirm({
  //     title: t("actions.deleteAnnouncement"),
  //     children: t("texts.deletionAnnouncementConfirmation"),
  //     confirmationText: t("actions.delete"),
  //   });

  //   if (result) {
  //     const { closeDialog, setIsLoading } = result;

  //     setIsLoading(true);
  //     const response = await deleteAnnouncement(id);

  //     if (response) {
  //       enqueueSnackbar(t("texts.announcementDeletingSuccess"), { variant: "success" });
  //     }

  //     closeDialog();
  //   }
  // };

  const handleCreateRegistrationRequest = async (params: ICreateRegistrationRequestDto) => {
    try {
      const response = await createRegistrationRequest(params);

      if (response) {
        enqueueSnackbar(t("texts.sendRequestSuccess"), { variant: "success" });
        closeDialog();
      }
    } finally {
      /* empty */
    }
  };

  const handleSendRequest = async ({ id, registration_form }: IAnnouncementDto) => {
    const { fields } = registration_form || {};

    if (fields && !isEmpty(fields)) {
      openDialog({
        title: t("actions.sendRequest"),
        children: (
          <RegistrationRequestForm
            fieldList={fields}
            onSubmit={(values) =>
              handleCreateRegistrationRequest({
                announcement_id: id,
                form_responses: Object.entries(values).map(([formFieldId, value]) => ({
                  form_field_id: +formFieldId,
                  value: value.toString(),
                })),
              })
            }
          />
        ),
      });
    } else {
      const result = await confirm({
        title: t("actions.sendRequest"),
        children: t("texts.sendRequestConfirmation"),
        confirmationText: t("actions.send"),
      });

      if (result) {
        handleCreateRegistrationRequest({ announcement_id: id });
      }
    }
  };

  useEffect(() => () => reactionList.forEach((reaction) => reaction()), []);

  // TODO оптимизировать рендер данных mobx - распихать на разные компоненты
  return (
    <>
      <MainPageImgStyled>
        <MainPageImgContentStyled>
          <T variant="h4" sx={{ maxWidth: { xs: "350px", md: "500px" } }}>
            {t("texts.mainTitleCompete")}{" "}
            <span style={{ color: theme.palette.primary.main }}>{t("texts.mainTitleWin")}</span>{" "}
            {t("texts.mainTitleImprove")}
          </T>
          <T variant="body2" sx={{ maxWidth: { xs: "350px", md: "550px" } }}>
            {t("texts.mainSubtitle")}
          </T>
        </MainPageImgContentStyled>
      </MainPageImgStyled>
      <PageWrapperStyled>
        <Badge badgeContent={listData.total} color="secondary">
          <T variant="h5" className="capitalize-first">
            {t("entities.announcement.many")}
          </T>
        </Badge>
        <AnnouncementsFilters filters={filters} handleFilter={setFilter} />
        <InfiniteScrollList
          renderItem={(item) => (
            <AnnouncementCard
              key={item.id}
              announcement={item}
              button={
                item.status === EAnnouncementStatuses.RegistrationOpen
                  ? {
                      title: t("actions.takePart"),
                      onClick: () => handleSendRequest(item),
                      icon: <SendOutlinedIcon />,
                    }
                  : undefined
              }
            />
          )}
          onLoadMore={paginate}
          {...listData}
        />
      </PageWrapperStyled>
    </>
  );
});
