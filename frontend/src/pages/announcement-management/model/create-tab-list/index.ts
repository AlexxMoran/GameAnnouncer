import type { ICreateTabListParams } from "@pages/announcement-management/model/create-tab-list/types";
import { EAnnouncementManagementTabs } from "@shared/constants/appRoutes";

export const createTabList = ({ t, isOrganizer }: ICreateTabListParams) => {
  const tabList = [];

  if (isOrganizer) {
    tabList.push({
      label: t("entities.bid.many"),
      value: EAnnouncementManagementTabs.Requests,
    });
  }

  tabList.push(
    { label: t("entities.qualification.one"), value: EAnnouncementManagementTabs.Qualification },
    { label: t("texts.tournamentBracket"), value: EAnnouncementManagementTabs.TournamentGrid },
    { label: t("entities.broadcast.one"), value: EAnnouncementManagementTabs.Broadcast }
  );

  return tabList;
};
