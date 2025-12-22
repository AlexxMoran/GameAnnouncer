import { AsyncPipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatDialog } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslatePipe } from '@ngx-translate/core';
import { IGame } from '@pages/games/model/game.types';
import { GameCard } from '@pages/games/ui/game-card/game-card';
import { GameCreationForm } from '@pages/games/ui/game-creation-form/game-creation-form';
import {
  ICreateGameDto,
  IGameDto,
  IGameListFilters,
  IUpdateGameDto,
} from '@shared/api/games/games-api-service.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { PaginationService } from '@shared/lib/pagination/pagination.service';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Chips } from '@shared/ui/chips/chips';
import { SUCCESS_CONFIRM_RESULT } from '@shared/ui/dialog-confirm-content/dialog-confirm-content.constants';
import { FabButton } from '@shared/ui/fab-button/fab-button';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-games-page',
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
  templateUrl: './games-page.html',
  host: { class: 'w-full h-full' },
})
export class GamesPage {
  private paginationService =
    inject<PaginationService<IGameDto, IGameListFilters>>(PaginationService);
  private gameApiService = inject(GamesApiService);
  private dialog = inject(MatDialog);
  private dialogService = inject(DialogService);
  private snackBarService = inject(SnackBarService);

  isLoading = signal<boolean>(false);
  list$ = this.paginationService.list$;

  getGameActionList = (game: IGame): IIconMenuOption[] => {
    return [
      { name: 'create', label: 'actions.createTournament' },
      {
        name: 'edit',
        label: 'actions.edit',
        click: () => this.openEditDialog(game),
      },
      { name: 'delete', label: 'actions.delete', click: () => this.deleteGame(game) },
    ];
  };

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
          this.snackBarService.showSuccessSnackBar('texts.gameAddingSuccess');
          this.paginationService.reset();
          this.dialog.closeAll();
        },
      });
  };

  editGame = (id: number, values: IUpdateGameDto) => {
    this.isLoading.set(true);

    this.gameApiService
      .editGame(id, values)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe(({ data }) => {
        this.snackBarService.showSuccessSnackBar('texts.gameEditingSuccess');
        this.paginationService.editEntity(data);
        this.dialog.closeAll();
      });
  };

  deleteGame = ({ id }: IGame) => {
    this.dialogService
      .confirm({ message: 'texts.deletionGameConfirmation' })
      .afterClosed()
      .subscribe((result) => {
        if (result === SUCCESS_CONFIRM_RESULT) {
          this.snackBarService.showSuccessSnackBar('texts.requestSendingSuccess');

          this.gameApiService.deleteGame(id).subscribe(() => {
            this.snackBarService.showSuccessSnackBar('texts.gameDeletingSuccess');
            this.paginationService.reset();
          });
        }
      });
  };

  openCreateDialog = () => {
    this.dialogService.open(GameCreationForm, {
      title: 'actions.addGame',
      inputs: {
        buttonText: 'actions.add',
        isLoading: this.isLoading,
      },
      outputs: { submitted: this.createGame },
    });
  };

  openEditDialog = (game: IGame) => {
    this.dialogService.open(GameCreationForm, {
      title: 'actions.editGame',
      inputs: {
        buttonText: 'actions.save',
        isLoading: this.isLoading,
        gameToUpdate: game,
      },
      outputs: { submitted: (values) => this.editGame(game.id, values) },
    });
  };
}
