import { Box } from "@mui/material";
import { AnnouncementManagementService } from "@pages/announcement-management/model/announcement-management-service";
import { createTabList } from "@pages/announcement-management/model/create-tab-list";
import type { IOutletContextData } from "@pages/announcement-management/model/types";
import { AnnouncementActions } from "@pages/announcement-management/ui/announcement-actions";
import { AnnouncementInfo } from "@pages/announcement-management/ui/announcement-info";
import { AnnouncementManagementPageHeader } from "@pages/announcement-management/ui/announcement-management-page-header";
import { useRootService } from "@shared/hooks/use-root-service";
import { useTabs } from "@shared/hooks/use-tabs";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { Spinner } from "@shared/ui/spinner";
import { Tabs } from "@shared/ui/tabs";
import { observer } from "mobx-react-lite";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";
import { Outlet, useParams } from "react-router";

export const AnnouncementManagementPage: FC = observer(() => {
  const { announcementsApiService, authService } = useRootService();
  const { handleChangeTab, tabValue } = useTabs();
  const { t } = useTranslation();
  const { id } = useParams();

  const [announcementManagementService] = useState(
    () => new AnnouncementManagementService(announcementsApiService, authService, id)
  );

  const { isLoading, announcement, isOrganizer, cancelAnnouncement, editAnnouncement, startAnnouncement } =
    announcementManagementService;

  const tabList = createTabList({ t, isOrganizer });

  if (isLoading) {
    return <Spinner type="backdrop" />;
  }

  return (
    <>
      <AnnouncementManagementPageHeader announcement={announcement} />
      <PageContentWrapperStyled>
        <Box sx={{ display: "flex", gap: { xs: 2, md: 3 }, flexDirection: { xs: "column", md: "row" } }}>
          <Box sx={{ flex: 1, order: { xs: 1, md: 0 } }}>
            <Tabs tabList={tabList} onChange={handleChangeTab} value={tabValue}>
              <Outlet context={{ announcement } as IOutletContextData} />
            </Tabs>
          </Box>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: { xs: 2, md: 3 },
              width: { md: "35%" },
              maxWidth: { md: "350px" },
              position: { md: "sticky" },
              top: 88,
              height: "fit-content",
              order: { xs: 0, md: 1 },
            }}
          >
            {isOrganizer && (
              <AnnouncementActions
                announcement={announcement}
                startAnnouncement={startAnnouncement}
                cancelAnnouncement={cancelAnnouncement}
                editAnnouncement={editAnnouncement}
              />
            )}
            <AnnouncementInfo announcement={announcement} />
          </Box>
        </Box>
      </PageContentWrapperStyled>
    </>
  );
});
