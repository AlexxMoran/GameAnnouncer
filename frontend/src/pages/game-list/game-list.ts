import { Component, inject, OnInit } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { GAMES_ENDPOINT } from '@entities/games/api/games-endpoints.const';
import { GameCard } from '@entities/games/ui/game-card/game-card';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { ENDPOINT, OffsetPaginationService } from '@shared/lib/api/offset-pagination.service';

@Component({
  selector: 'game-list',
  imports: [GameCard, MatProgressSpinnerModule, ElementObserverDirective],
  providers: [
    OffsetPaginationService,
    {
      provide: ENDPOINT,
      useValue: GAMES_ENDPOINT,
    },
  ],
  templateUrl: './game-list.html',
  styleUrl: './game-list.scss',
  host: { class: 'flex flex-col items-center gap-10 w-full h-full' },
})
export class GameList implements OnInit {
  gameListService = inject(OffsetPaginationService);

  ngOnInit() {
    this.gameListService.initDataLoading();
  }

  get gameList() {
    return this.gameListService.list;
  }

  get canPaginate() {
    return this.gameListService.canPaginate();
  }

  get isPaginating() {
    return this.gameListService.isPaginating();
  }

  get isInitializeLoading() {
    return this.gameListService.isInitializeLoading();
  }
}
