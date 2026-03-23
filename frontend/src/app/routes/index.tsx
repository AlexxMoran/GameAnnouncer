import { AccountSettingsPage } from "@pages/account-settings/ui/account-settings-page";
import { AnnouncementsPage } from "@pages/announcements/ui/announcements-page";
import { EmailVerificationPage } from "@pages/email-verification/ui/email-verification-page";
import { GamesPage } from "@pages/games/ul/games-page";
import { LoginPage } from "@pages/login/ui/login-page";
import { AnnouncementsTab } from "@pages/my-announcements/ui/announcements-tab";
import { MyAnnouncementsPage } from "@pages/my-announcements/ui/my-announcements-page";
import { NotFoundPage } from "@pages/not-found/ui/not-found-page";
import { RegistrationRequestsPage } from "@pages/registration-requests/ui/registration-requests-page";
import { RegistrationPage } from "@pages/registration/ui/registration-page";
import { EAppRoutes, EMyAnnouncementsTabs } from "@shared/constants/appRoutes";
import withAuth from "@shared/hocs/with-auth";
import type { FC } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router";

const AccountSettingsPageWithAuth = withAuth(AccountSettingsPage);
const MyAnnouncementsPageWithAuth = withAuth(MyAnnouncementsPage);
const RegistrationRequestsPageWithAuth = withAuth(RegistrationRequestsPage);

export const Pages: FC = () => {
  const location = useLocation();

  return (
    <Routes>
      <Route path="/" element={<Navigate to={EAppRoutes.Announcements} replace />} />
      <Route path={EAppRoutes.Announcements} element={<AnnouncementsPage />} />
      <Route path={EAppRoutes.Games} element={<GamesPage />} />
      <Route path={EAppRoutes.Login} element={<LoginPage />} />
      <Route path={EAppRoutes.Registration} element={<RegistrationPage />} />
      <Route path={EAppRoutes.AccountSettings} element={<AccountSettingsPageWithAuth />} />
      <Route path={EAppRoutes.VerifyEmail} element={<EmailVerificationPage />} />
      <Route path={EAppRoutes.MyAnnouncements} element={<MyAnnouncementsPageWithAuth />}>
        <Route index element={<Navigate to={EMyAnnouncementsTabs.Participated} replace />} />
        <Route path={EMyAnnouncementsTabs.Participated} element={<AnnouncementsTab key={location.pathname} />} />
        <Route
          path={EMyAnnouncementsTabs.Organized}
          element={<AnnouncementsTab key={location.pathname} canAddAnnouncements />}
        />
      </Route>
      <Route path={EAppRoutes.RegistrationRequests} element={<RegistrationRequestsPageWithAuth />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
