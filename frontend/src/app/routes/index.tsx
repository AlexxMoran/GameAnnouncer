import { AccountSettingsPage } from "@pages/account-settings/ui/account-settings-page";
import { AnnouncementsPage } from "@pages/announcements/ui/announcements-page";
import { EmailVerificationPage } from "@pages/email-verification/ui/email-verification-page";
import { GamesPage } from "@pages/games/ul/games-page";
import { LoginPage } from "@pages/login/ui/login-page";
import { AnnouncementsTab } from "@pages/my-announcements/ui/announcements-tab";
import { MyAnnouncementsPage } from "@pages/my-announcements/ui/my-announcements-page";
import { NotFoundPage } from "@pages/not-found/ui/not-found-page";
import { RegistrationPage } from "@pages/registration/ui/registration-page";
import { EAppRoutes, EAppSubRoutes } from "@shared/constants/appRoutes";
import type { FC } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router";

export const Pages: FC = () => {
  const location = useLocation();

  return (
    <Routes>
      <Route
        path="/"
        element={<Navigate to={EAppRoutes.Announcements} replace />}
      />
      <Route path={EAppRoutes.Announcements} element={<AnnouncementsPage />} />
      <Route path={EAppRoutes.Games} element={<GamesPage />} />
      <Route path={EAppRoutes.Login} element={<LoginPage />} />
      <Route path={EAppRoutes.Registration} element={<RegistrationPage />} />
      <Route
        path={EAppRoutes.AccountSettings}
        element={<AccountSettingsPage />}
      />
      <Route
        path={EAppRoutes.VerifyEmail}
        element={<EmailVerificationPage />}
      />
      <Route
        path={EAppRoutes.MyAnnouncements}
        element={<MyAnnouncementsPage />}
      >
        <Route
          index
          element={
            <Navigate to={EAppSubRoutes.ParticipatedAnnouncements} replace />
          }
        />
        <Route
          path={EAppSubRoutes.ParticipatedAnnouncements}
          element={<AnnouncementsTab key={location.pathname} />}
        />
        <Route
          path={EAppSubRoutes.OrganizedAnnouncements}
          element={<AnnouncementsTab key={location.pathname} />}
        />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
