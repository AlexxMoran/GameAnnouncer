import { Routes } from '@angular/router';
import { GamesPage } from '@pages/games/ui/games-page/games-page';
import { Login } from '@pages/login/login';
import { Registration } from '@pages/registration/registration';
import { NotFoundPage } from 'src/pages/not-found-page/not-found-page';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'games',
    pathMatch: 'full',
  },
  {
    path: 'login',
    component: Login,
  },
  {
    path: 'registration',
    component: Registration,
  },
  {
    path: 'games',
    component: GamesPage,
  },
  { path: '**', component: NotFoundPage },
];
