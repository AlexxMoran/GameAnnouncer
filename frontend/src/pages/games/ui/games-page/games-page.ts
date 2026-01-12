import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslatePipe } from '@ngx-translate/core';
import { createGameCreationFormInputs } from '@pages/games/model/create-game-creation-form-inputs';
import { createGameEditingFormInputs } from '@pages/games/model/create-game-editing-form-inputs';
import { ICreateGameParams, IEditGameParams } from '@pages/games/model/game-creation-form.types';
import { IGame } from '@pages/games/model/game.types';
import { GameCard } from '@pages/games/ui/game-card/game-card';
import { IGameDto, IGameListFilters } from '@shared/api/games/games-api-service.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { GamesApiService } from '@shared/api/games/games-api.service';
import { ElementObserverDirective } from '@shared/directives/element-observer.directive';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { ListService } from '@shared/lib/list-service/list.service';
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
    FabButton,
    GameCard,
    Chips,
  ],
  templateUrl: './games-page.html',
  host: { class: 'w-full h-full' },
})
export class GamesPage implements OnInit, OnDestroy {
  private listService = new ListService<IGameDto, IGameListFilters>({
    loadDataFn: (params) => this.gameApiService.getGameList(params),
  });

  private gameApiService = inject(GamesApiService);
  private dialogService = inject(DialogService);
  private snackBarService = inject(SnackBarService);

  ngOnInit() {
    this.listService.init();
  }

  ngOnDestroy() {
    this.listService.destroy();
  }

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
    return this.listService.isInitializeLoading();
  }

  get isPaginating() {
    return this.listService.isPaginating();
  }

  get hasNoData() {
    return this.listService.hasNoData();
  }

  get chipList() {
    return Object.entries(EGameCategories).map(([label, name]) => ({ label, name }));
  }

  get total() {
    return this.listService.total();
  }

  get gameList() {
    return this.listService.list();
  }

  paginate = this.listService.paginate;

  addGameFilters = (selectedChipName: TMaybe<string>) => {
    if (selectedChipName) {
      this.listService.addFilters({ category: selectedChipName as EGameCategories });
    } else {
      this.listService.clearFilters();
    }
  };

  createGame = (values: ICreateGameParams) => {
    return this.gameApiService.createGame(values).pipe(
      tap(() => {
        this.snackBarService.showSuccessSnackBar('texts.gameAddingSuccess');
        this.listService.resetList();
      }),
    );
  };

  editGame = (id: number, values: IEditGameParams) => {
    return this.gameApiService.editGame(id, values).pipe(
      tap(({ data }) => {
        this.snackBarService.showSuccessSnackBar('texts.gameEditingSuccess');
        this.listService.editEntity(data);
      }),
    );
  };

  uploadGameImage = (id: number, file: File) => {
    return this.gameApiService.uploadGameImage(id, file).pipe(
      tap(({ data }) => {
        this.snackBarService.showSuccessSnackBar('texts.gameUploadSuccess');
        this.listService.editEntity(data);
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
          this.listService.resetList();
        }),
      ),
    });
  };

  openCreateDialog = () => {
    this.dialogService.open(Form<ICreateGameParams>, {
      title: 'actions.addGame',
      inputs: {
        ...createGameCreationFormInputs(),
        buttonText: 'actions.add',
        createSubmitObservableFn: (values) => this.createGame(values),
      },
    });
  };

  openEditDialog = (game: IGame) => {
    this.dialogService.open(Form<IEditGameParams>, {
      title: 'actions.editGame',
      inputs: {
        ...createGameEditingFormInputs(),
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
