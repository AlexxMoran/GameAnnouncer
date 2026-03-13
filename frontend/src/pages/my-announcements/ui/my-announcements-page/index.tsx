import { EMyAnnouncementsTabs } from "@shared/constants/appRoutes";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { PageTitle } from "@shared/ui/page-title";
import { Tabs } from "@shared/ui/tabs";
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
        navigate(EMyAnnouncementsTabs.Participated);

        break;
      }

      case EMyAnnouncementsTabs.Organized: {
        navigate(EMyAnnouncementsTabs.Organized);

        break;
      }
    }
  };

  return (
    <PageContentWrapperStyled>
      <PageTitle title={t("texts.myAnnouncementsTitle")} />
      <Tabs tabList={tabList} onChange={handleChangeTab} value={pathParts.at(-1)}>
        <Outlet />
      </Tabs>
    </PageContentWrapperStyled>
  );
};
