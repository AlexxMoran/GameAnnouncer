import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslatePipe } from '@ngx-translate/core';
import { ANNOUNCEMENT_CREATION_FORM_INPUTS } from '@pages/announcements/model/announcement-creation-form.constants';
import { ICreateAnnouncementParams } from '@pages/announcements/model/announcement-creation-form.types';
import { AnnouncementCard } from '@pages/announcements/ui/announcement-card/announcement-card';
import {
  IAnnouncementDto,
  IAnnouncementListFilters,
} from '@shared/api/announcements/announcements-api-service.types';
import { AnnouncementApiService } from '@shared/api/announcements/announcements-api.service';
import { DialogService } from '@shared/lib/dialog/dialog.service';
import { ListService } from '@shared/lib/list-service/list.service';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { FabButton } from '@shared/ui/fab-button/fab-button';
import { Form } from '@shared/ui/form/form';

@Component({
  selector: 'app-announcements-page',
  imports: [MatProgressSpinnerModule, AnnouncementCard, TranslatePipe, MatBadgeModule, FabButton],
  templateUrl: './announcements-page.html',
})
export class AnnouncementsPage implements OnInit, OnDestroy {
  private listService = new ListService<IAnnouncementDto, IAnnouncementListFilters>({
    loadDataFn: (params) => this.announcementApiService.getAnnouncementList(params!),
  });

  private announcementApiService = inject(AnnouncementApiService);
  private dialogService = inject(DialogService);
  private snackBarService = inject(SnackBarService);

  ngOnInit() {
    this.listService.init();
  }

  ngOnDestroy() {
    this.listService.destroy();
  }

  get isInitializeLoading() {
    return this.listService.isInitializeLoading();
  }

  get isPaginating() {
    return this.listService.isPaginating();
  }

  get hasNoData() {
    return this.listService.hasNoData();
  }

  get total() {
    return this.listService.total();
  }

  get announcementList() {
    return this.listService.list();
  }

  paginate = this.listService.paginate;

  openCreateDialog = () => {
    this.dialogService.open(Form<ICreateAnnouncementParams>, {
      title: 'actions.addGame',
      inputs: {
        ...ANNOUNCEMENT_CREATION_FORM_INPUTS,
        buttonText: 'actions.add',
        // createSubmitObservableFn: (values) => this.createGame(values),
      },
    });
  };
}
