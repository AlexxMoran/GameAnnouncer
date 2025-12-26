import { AsyncPipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslatePipe } from '@ngx-translate/core';
import {
  GAME_CREATION_FORM_INPUTS,
  GAME_EDITING_FORM_INPUTS,
} from '@pages/games/model/game-creation-form.constants';
import { ICreateGameParams, IEditGameParams } from '@pages/games/model/game-creation-form.types';
import { IGame } from '@pages/games/model/game.types';
import { GameCard } from '@pages/games/ui/game-card/game-card';
import { IGameDto, IGameListFilters } from '@shared/api/games/games-api-service.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { PaginationService } from '@shared/lib/pagination/pagination.service';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Chips } from '@shared/ui/chips/chips';
import { FabButton } from '@shared/ui/fab-button/fab-button';
import { Form } from '@shared/ui/form/form';
import { ImageCropper } from '@shared/ui/image-cropper/image-cropper';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';
import { tap } from 'rxjs';

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
  private dialogService = inject(DialogService);
  private snackBarService = inject(SnackBarService);

  list$ = this.paginationService.list$;

  getGameActionList = (game: IGame): IIconMenuOption[] => {
    return [
      { name: 'create', label: 'actions.createTournament' },
      {
        name: 'uploadImage',
        label: 'actions.uploadImage',
        click: () => this.openUploadImageModal(game),
      },
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

  createGame = (values: ICreateGameParams) => {
    return this.gameApiService.createGame(values).pipe(
      tap(() => {
        this.snackBarService.showSuccessSnackBar('texts.gameAddingSuccess');
        this.paginationService.reset();
      }),
    );
  };

  editGame = (id: number, values: IEditGameParams) => {
    return this.gameApiService.editGame(id, values).pipe(
      tap(({ data }) => {
        this.snackBarService.showSuccessSnackBar('texts.gameEditingSuccess');
        this.paginationService.editEntity(data);
      }),
    );
  };

  uploadGameImage = (id: number, file: File) => {
    return this.gameApiService.uploadGameImage(id, file).pipe(
      tap(({ data }) => {
        this.snackBarService.showSuccessSnackBar('texts.gameUploadSuccess');
        this.paginationService.editEntity(data);
      }),
    );
  };

  deleteGame = ({ id }: IGame) => {
    this.dialogService.confirm({
      message: 'texts.deletionGameConfirmation',
      confirmButtonText: 'actions.delete',
      confirmObservable: this.gameApiService.deleteGame(id).pipe(
        tap(() => {
          this.snackBarService.showSuccessSnackBar('texts.gameDeletingSuccess');
          this.paginationService.reset();
        }),
      ),
    });
  };

  openCreateDialog = () => {
    this.dialogService.open(Form<ICreateGameParams>, {
      title: 'actions.addGame',
      inputs: {
        ...GAME_CREATION_FORM_INPUTS,
        buttonText: 'actions.add',
        createSubmitObservableFn: (values) => this.createGame(values),
      },
    });
  };

  openEditDialog = (game: IGame) => {
    this.dialogService.open(Form<IEditGameParams>, {
      title: 'actions.editGame',
      inputs: {
        ...GAME_EDITING_FORM_INPUTS,
        buttonText: 'actions.save',
        initialValues: game,
        createSubmitObservableFn: (values) => this.editGame(game.id, values),
      },
    });
  };

  openUploadImageModal = (game: IGame) => {
    this.dialogService.open(ImageCropper, {
      title: 'actions.uploadImage',
      inputs: {
        buttonText: 'actions.upload',
        createUploadObserver: (file) => this.uploadGameImage(game.id, file),
      },
    });
  };
}
