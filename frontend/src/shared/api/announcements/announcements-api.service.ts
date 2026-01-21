import { inject, Injectable } from '@angular/core';
import { ANNOUNCEMENTS_ENDPOINT } from '@shared/api/announcements/announcements-api-service.constants';
import {
  IAnnouncementDto,
  ICreateAnnouncementDto,
  IEditAnnouncementDto,
  IGetAnnouncementListDto,
} from '@shared/api/announcements/announcements-api-service.types';
import { TApiResponseWrapper } from '@shared/api/base-api-service.types';
import { BaseApiService } from '@shared/api/base-api.service';
import { IPaginationMeta } from '@shared/lib/list-service/list-service.types';

@Injectable({ providedIn: 'root' })
export class AnnouncementApiService {
  private baseApiService = inject(BaseApiService);

  getAnnouncementList = (params: IGetAnnouncementListDto) => {
    return this.baseApiService.get<TApiResponseWrapper<IAnnouncementDto[]>, IPaginationMeta>(
      ANNOUNCEMENTS_ENDPOINT,
      { params },
    );
  };

  createAnnouncement = (params: ICreateAnnouncementDto) => {
    return this.baseApiService.post<TApiResponseWrapper<IAnnouncementDto>>(
      ANNOUNCEMENTS_ENDPOINT,
      params,
    );
  };

  editAnnouncement = (id: number, params: IEditAnnouncementDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IAnnouncementDto>>(
      `${ANNOUNCEMENTS_ENDPOINT}/${id}`,
      params,
    );
  };

  deleteAnnouncement = (id: number) => {
    return this.baseApiService.delete<TApiResponseWrapper<IAnnouncementDto>>(
      `${ANNOUNCEMENTS_ENDPOINT}/${id}`,
    );
  };
}
