import { EMyAnnouncementsTabs } from "@pages/my-announcements/ui/my-announcements-page/constants";
import { EAppSubRoutes } from "@shared/constants/appRoutes";
import { Box } from "@shared/ui/box";
import { Tabs } from "@shared/ui/tabs";
import { T } from "@shared/ui/typography";
import type { FC, SyntheticEvent } from "react";
import { useTranslation } from "react-i18next";
import { Outlet, useLocation, useNavigate } from "react-router";

export const MyAnnouncementsPage: FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  const pathParts = location.pathname.split("/");

  const tabList = [
    {
      label: t("entities.participant"),
      value: EMyAnnouncementsTabs.Participated,
    },
    { label: t("entities.organizer"), value: EMyAnnouncementsTabs.Organized },
  ];

  const handleChangeTab = (_: SyntheticEvent, value: EMyAnnouncementsTabs) => {
    switch (value) {
      case EMyAnnouncementsTabs.Participated: {
        navigate(EAppSubRoutes.ParticipatedAnnouncements);

        break;
      }
      case EMyAnnouncementsTabs.Organized: {
        navigate(EAppSubRoutes.OrganizedAnnouncements);
      }
    }
  };

  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <T variant="h4">{t("texts.myAnnouncementsTitle")}</T>
      <Tabs
        tabList={tabList}
        onChange={handleChangeTab}
        value={pathParts.at(-1)}
      >
        <Outlet />
      </Tabs>
    </Box>
  );
};
