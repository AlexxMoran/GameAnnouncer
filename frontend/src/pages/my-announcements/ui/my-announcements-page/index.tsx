import { EMyAnnouncementsTabs } from "@shared/constants/appRoutes";
import { useTabs } from "@shared/hooks/use-tabs";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { PageTitle } from "@shared/ui/page-title";
import { Tabs } from "@shared/ui/tabs";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { Outlet } from "react-router";

export const MyAnnouncementsPage: FC = () => {
  const { t } = useTranslation();
  const { handleChangeTab, tabValue } = useTabs();

  const tabList = [
    {
      label: t("entities.participant"),
      value: EMyAnnouncementsTabs.Participated,
    },
    { label: t("entities.organizer"), value: EMyAnnouncementsTabs.Organized },
  ];

  return (
    <PageContentWrapperStyled>
      <PageTitle title={t("texts.myAnnouncementsTitle")} />
      <Tabs tabList={tabList} onChange={handleChangeTab} value={tabValue}>
        <Outlet />
      </Tabs>
    </PageContentWrapperStyled>
  );
};
