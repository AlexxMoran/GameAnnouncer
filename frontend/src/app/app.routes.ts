import { Routes } from '@angular/router';
import { AnnouncementsPage } from '@pages/announcements/ui/announcements-page/announcements-page';
import { EmailVerificationPage } from '@pages/email-verification/ui/email-verification-page/email-verification-page';
import { GamesPage } from '@pages/games/ui/games-page/games-page';
import { LoginPage } from '@pages/login/ui/login-page/login-page';
import { RegistrationPage } from '@pages/registration/ui/registration-page/registration-page';
import { EAppRoutes } from '@shared/routes/routes.constants';
import { NotFoundPage } from 'src/pages/not-found-page/not-found-page';

export const routes: Routes = [
  {
    path: '',
    redirectTo: EAppRoutes.Announcements,
    pathMatch: 'full',
  },
  {
    path: EAppRoutes.Login,
    component: LoginPage,
  },
  {
    path: EAppRoutes.Registration,
    component: RegistrationPage,
  },
  {
    path: EAppRoutes.VerifyEmail,
    component: EmailVerificationPage,
  },
  {
    path: EAppRoutes.Announcements,
    component: AnnouncementsPage,
  },
  {
    path: EAppRoutes.Games,
    component: GamesPage,
  },
  { path: '**', component: NotFoundPage },
];
