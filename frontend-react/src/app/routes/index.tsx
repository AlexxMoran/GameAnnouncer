import { AccountSettingsPage } from "@pages/account-settings/ui/account-settings-page";
import { AnnouncementsPage } from "@pages/announcements/ui/announcements-page";
import { EmailVerificationPage } from "@pages/email-verification/ui/email-verification-page";
import { GamesPage } from "@pages/games/ul/games-page";
import { LoginPage } from "@pages/login/ui/login-page";
import { NotFoundPage } from "@pages/not-found/ui/not-found-page";
import { RegistrationPage } from "@pages/registration/ui/registration-page";
import { EAppRoutes } from "@shared/constants/appRoutes";
import type { FC } from "react";
import { Navigate, Route, Routes } from "react-router";

export const Pages: FC = () => {
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
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
