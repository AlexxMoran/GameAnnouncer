import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { GameCard } from '@entities/game/ui/game-card/game-card';
import { TranslatePipe } from '@ngx-translate/core';
import { EGameCategories } from '@shared/api/games/games-api.const';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { IGameDto, IGameListFilters } from '@shared/api/games/games-api.types';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { PaginationService } from '@shared/lib/pagination/pagination.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Chips } from '@shared/ui/chips/chips';

@Component({
  selector: 'app-game-list',
  imports: [
    GameCard,
    MatProgressSpinnerModule,
    Chips,
    ElementObserverDirective,
    AsyncPipe,
    TranslatePipe,
  ],
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
  host: { class: 'w-full h-full' },
})
export class GameList {
  private paginationService =
    inject<PaginationService<IGameDto, IGameListFilters>>(PaginationService);
  list$ = this.paginationService.list$;
  paginate = this.paginationService.paginate;

  get isInitializeLoading() {
    return this.paginationService.isInitializeLoading();
  }

  get isPaginating() {
    return this.paginationService.isPaginating();
  }

  get hasNoData() {
    return this.paginationService.total() === 0;
  }

  get chipList() {
    return Object.entries(EGameCategories).map(([label, name]) => ({ label, name }));
  }

  addGameFilters(selectedChipName: TMaybe<string>) {
    if (selectedChipName) {
      this.paginationService.addFilters({ category: selectedChipName as EGameCategories });
    } else {
      this.paginationService.clearFilters();
    }
  }
}
