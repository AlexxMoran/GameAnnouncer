import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { GameCard } from '@entities/game/ui/game-card/game-card';
import { TranslatePipe } from '@ngx-translate/core';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { IGameDto } from '@shared/api/games/games-api.types';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { PaginationService } from '@shared/lib/pagination/pagination.service';

@Component({
  selector: 'app-game-list',
  imports: [GameCard, MatProgressSpinnerModule, ElementObserverDirective, AsyncPipe, TranslatePipe],
  providers: [
    {
      provide: PaginationService,
      useFactory: () => {
        const gamesApiService = inject(GamesApiService);

        return new PaginationService({
          loadDataFn: gamesApiService.getGameList.bind(gamesApiService),
        });
      },
    },
  ],
  templateUrl: './game-list.html',
  host: { class: 'flex flex-col w-full h-full' },
})
export class GameList {
  gameListService = inject<PaginationService<IGameDto>>(PaginationService);

  list$ = this.gameListService.list$;
  paginate = this.gameListService.paginate;

  get isInitializeLoading() {
    return this.gameListService.isInitializeLoading();
  }

  get isPaginating() {
    return this.gameListService.isPaginating();
  }

  get hasNoData() {
    return !this.gameListService.total() && !this.isInitializeLoading;
  }
}
