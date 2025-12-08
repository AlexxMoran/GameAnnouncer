import { Component, inject, OnInit } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { GameCard } from '@entities/game/ui/game-card/game-card';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { OffsetPaginationService } from '@shared/lib/pagination/offset-pagination.service';

@Component({
  selector: 'app-game-list',
  imports: [GameCard, MatProgressSpinnerModule, ElementObserverDirective],
  providers: [
    {
      provide: OffsetPaginationService,
      useFactory: () => {
        const gamesApiService = inject(GamesApiService);

        return new OffsetPaginationService({
          loadDataFn: gamesApiService.getGameList.bind(gamesApiService),
        });
      },
    },
  ],
  templateUrl: './game-list.html',
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
