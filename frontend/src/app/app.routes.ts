import { Routes } from '@angular/router';
import { EmailVerificationPage } from '@pages/email-verification/ui/email-verification-page/email-verification-page';
import { GamesPage } from '@pages/games/ui/games-page/games-page';
import { LoginPage } from '@pages/login/ui/login-page/login-page';
import { RegistrationPage } from '@pages/registration/ui/registration-page/registration-page';
import { NotFoundPage } from 'src/pages/not-found-page/not-found-page';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'games',
    pathMatch: 'full',
  },
  {
    path: 'login',
    component: LoginPage,
  },
  {
    path: 'registration',
    component: RegistrationPage,
  },
  {
    path: 'games',
    component: GamesPage,
  },
  {
    path: 'verify-email',
    component: EmailVerificationPage,
  },
  { path: '**', component: NotFoundPage },
];
