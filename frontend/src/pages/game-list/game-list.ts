import { AsyncPipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatDialog } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { GameCard } from '@entities/game/ui/game-card/game-card';
import { CreateGameForm } from '@features/create-game/ui/create-game-form/create-game-form';
import { TranslatePipe } from '@ngx-translate/core';
import { EGameCategories } from '@shared/api/games/games-api.const';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { ICreateGameDto, IGameDto, IGameListFilters } from '@shared/api/games/games-api.types';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { PaginationService } from '@shared/lib/pagination/pagination.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Chips } from '@shared/ui/chips/chips';
import { FabButton } from '@shared/ui/fab-button/fab-button';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-game-list',
  imports: [
    MatProgressSpinnerModule,
    ElementObserverDirective,
    MatBadgeModule,
    TranslatePipe,
    AsyncPipe,
    FabButton,
    GameCard,
    Chips,
  ],
  providers: [
    {
      provide: PaginationService,
      useFactory: () => {
        const gamesApiService = inject(GamesApiService);

        return new PaginationService({
          loadDataFn: gamesApiService.getGameList,
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
  private gameApiService = inject(GamesApiService);
  private dialog = inject(MatDialog);
  private dialogService = inject(DialogService);

  isLoading = signal<boolean>(false);

  readonly gameActionList = [{ name: 'create', label: 'actions.createTournament' }];
  list$ = this.paginationService.list$;

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

  get total() {
    return this.paginationService.total();
  }

  paginate = this.paginationService.paginate;

  addGameFilters = (selectedChipName: TMaybe<string>) => {
    if (selectedChipName) {
      this.paginationService.addFilters({ category: selectedChipName as EGameCategories });
    } else {
      this.paginationService.clearFilters();
    }
  };

  createGame = (values: ICreateGameDto) => {
    this.isLoading.set(true);

    this.gameApiService
      .createGame(values)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        complete: () => {
          this.paginationService.reset();
          this.dialog.closeAll();
        },
      });
  };

  openCreateDialog = () => {
    this.dialogService.open(CreateGameForm, {
      title: 'actions.addGame',
      inputs: {
        buttonText: 'actions.add',
        isLoading: this.isLoading,
      },
      outputs: { submitted: this.createGame },
    });
  };
}
