import { AnnouncementCard } from "@entities/announcement/ui/announcement-card";
import SendOutlinedIcon from "@mui/icons-material/SendOutlined";
import { useAnnouncementsService } from "@pages/announcements/model/use-announcements-service";
import { useCreateRegistrationRequest } from "@pages/announcements/model/use-create-registration-request";
import { AnnouncementsFilters } from "@pages/announcements/ui/announcements-filters";
import { AnnouncementsWelcomeImg } from "@pages/announcements/ui/announcements-welcome-img";
import { EAnnouncementStatuses } from "@shared/services/api/announcements-api-service/constants";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { PageTitle } from "@shared/ui/page-title";
import { observer } from "mobx-react-lite";
import { useCallback, type FC } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementsPage: FC = observer(() => {
  const { handleCreateRegistrationRequest } = useCreateRegistrationRequest();
  const { listData, filters, setFilter, paginate } = useAnnouncementsService();
  const { t } = useTranslation();

  const renderItem = useCallback(
    (announcement: IAnnouncementDto) => (
      <AnnouncementCard
        key={announcement.id}
        announcement={announcement}
        button={
          announcement.status === EAnnouncementStatuses.RegistrationOpen
            ? {
                title: t("actions.takePart"),
                onClick: () => handleCreateRegistrationRequest(announcement),
                icon: <SendOutlinedIcon />,
              }
            : undefined
        }
      />
    ),
    [t, handleCreateRegistrationRequest]
  );

  return (
    <>
      <AnnouncementsWelcomeImg />
      <PageContentWrapperStyled>
        <PageTitle title={t("entities.announcement.many")} count={listData.filteredCount} />
        <AnnouncementsFilters filters={filters} handleFilter={setFilter} />
        <InfiniteScrollList renderItem={renderItem} onLoadMore={paginate} {...listData} />
      </PageContentWrapperStyled>
    </>
  );
});
