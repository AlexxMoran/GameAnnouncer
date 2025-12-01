import { Routes } from '@angular/router';
import { GameList } from 'src/pages/game-list/game-list';
import { NotFoundPage } from 'src/pages/not-found-page/not-found-page';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'games',
    pathMatch: 'full',
  },
  {
    path: 'games',
    component: GameList,
  },
  { path: '**', component: NotFoundPage },
];
