import { Routes } from '@angular/router';
import { Login } from '@pages/login/login';
import { Registration } from '@pages/registration/registration';
import { GameList } from 'src/pages/game-list/game-list';
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
    component: GameList,
  },
  { path: '**', component: NotFoundPage },
];
