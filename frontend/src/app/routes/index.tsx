import { App } from "@app/index";
import { AccountSettingsPage } from "@pages/account-settings/ui/account-settings-page";
import { AnnouncementBroadcast } from "@pages/announcement-management/ui/announcement-broadcast";
import { AnnouncementManagementPage } from "@pages/announcement-management/ui/announcement-management-page";
import { AnnouncementQualification } from "@pages/announcement-management/ui/announcement-qualification";
import { AnnouncementRequests } from "@pages/announcement-management/ui/announcement-requests";
import { AnnouncementTournamentBracket } from "@pages/announcement-management/ui/announcement-tournament-bracket";
import { AnnouncementsPage } from "@pages/announcements/ui/announcements-page";
import { EmailVerificationPage } from "@pages/email-verification/ui/email-verification-page";
import { GamesPage } from "@pages/games/ul/games-page";
import { LoginPage } from "@pages/login/ui/login-page";
import { AnnouncementsTab } from "@pages/my-announcements/ui/announcements-tab";
import { MyAnnouncementsPage } from "@pages/my-announcements/ui/my-announcements-page";
import { NotFoundPage } from "@pages/not-found/ui/not-found-page";
import { RegistrationRequestsPage } from "@pages/registration-requests/ui/registration-requests-page";
import { RegistrationPage } from "@pages/registration/ui/registration-page";
import { EAnnouncementManagementTabs, EAppRoutes, EMyAnnouncementsTabs } from "@shared/constants/appRoutes";
import withAuth from "@shared/hocs/with-auth";
import { createBrowserRouter, Navigate } from "react-router";

const AccountSettingsPageWithAuth = withAuth(AccountSettingsPage);
const MyAnnouncementsPageWithAuth = withAuth(MyAnnouncementsPage);
const RegistrationRequestsPageWithAuth = withAuth(RegistrationRequestsPage);

export const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      {
        path: "/",
        element: <Navigate to={EAppRoutes.Announcements} replace />,
      },
      {
        path: EAppRoutes.AnnouncementManagement,
        element: <AnnouncementManagementPage />,
        children: [
          { index: true, element: <Navigate to={EAnnouncementManagementTabs.Requests} replace /> },
          { path: EAnnouncementManagementTabs.Requests, element: <AnnouncementRequests /> },
          { path: EAnnouncementManagementTabs.Qualification, element: <AnnouncementQualification /> },
          { path: EAnnouncementManagementTabs.TournamentGrid, element: <AnnouncementTournamentBracket /> },
          { path: EAnnouncementManagementTabs.Broadcast, element: <AnnouncementBroadcast /> },
        ],
      },
      { path: EAppRoutes.Announcements, element: <AnnouncementsPage /> },
      { path: EAppRoutes.Games, element: <GamesPage /> },
      { path: EAppRoutes.Login, element: <LoginPage /> },
      { path: EAppRoutes.Registration, element: <RegistrationPage /> },
      { path: EAppRoutes.AccountSettings, element: <AccountSettingsPageWithAuth /> },
      { path: EAppRoutes.VerifyEmail, element: <EmailVerificationPage /> },
      {
        path: EAppRoutes.MyAnnouncements,
        element: <MyAnnouncementsPageWithAuth />,
        children: [
          { index: true, element: <Navigate to={EMyAnnouncementsTabs.Participated} replace /> },
          { path: EMyAnnouncementsTabs.Participated, element: <AnnouncementsTab /> },
          { path: EMyAnnouncementsTabs.Organized, element: <AnnouncementsTab canAddAnnouncements /> },
        ],
      },
      { path: EAppRoutes.RegistrationRequests, element: <RegistrationRequestsPageWithAuth /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
