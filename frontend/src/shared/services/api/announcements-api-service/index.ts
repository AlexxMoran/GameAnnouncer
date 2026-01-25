import {
  ANNOUNCEMENTS_ENDPOINT,
  USER_ANNOUNCEMENTS_ENDPOINT,
} from "@shared/services/api/announcements-api-service/constants";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
  IEditAnnouncementDto,
  IGetAnnouncementsDto,
  IGetOrganizedAnnouncementsDto,
  IGetParticipatedAnnouncementsDto,
} from "@shared/services/api/announcements-api-service/types";
import type { BaseApiService } from "@shared/services/api/base-api-service";
import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type { IPaginationMeta } from "@shared/types/pagination.types";

export class AnnouncementsApiService {
  constructor(private baseApiService: BaseApiService) {}

  getAnnouncements = (params: IGetAnnouncementsDto) => {
    return this.baseApiService.get<
      TApiResponseWrapper<IAnnouncementDto[]>,
      IPaginationMeta
    >(`/v1/${ANNOUNCEMENTS_ENDPOINT}`, { params });
  };

  createAnnouncement = (params: ICreateAnnouncementDto) => {
    return this.baseApiService.post<TApiResponseWrapper<IAnnouncementDto>>(
      `/v1/${ANNOUNCEMENTS_ENDPOINT}`,
      params
    );
  };

  editAnnouncement = (id: number, params: IEditAnnouncementDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IAnnouncementDto>>(
      `/v1/${ANNOUNCEMENTS_ENDPOINT}/${id}`,
      params
    );
  };

  deleteAnnouncement = (id: number) => {
    return this.baseApiService.delete<TApiResponseWrapper<IAnnouncementDto>>(
      `/v1/${ANNOUNCEMENTS_ENDPOINT}/${id}`
    );
  };

  getParticipatedAnnouncements = (params: IGetParticipatedAnnouncementsDto) => {
    return this.baseApiService.get<
      TApiResponseWrapper<IAnnouncementDto[]>,
      IPaginationMeta
    >(`/v1/${USER_ANNOUNCEMENTS_ENDPOINT}/participated_announcements`, {
      params,
    });
  };

  getOrganizedAnnouncements = (params: IGetOrganizedAnnouncementsDto) => {
    return this.baseApiService.get<
      TApiResponseWrapper<IAnnouncementDto[]>,
      IPaginationMeta
    >(`/v1/${USER_ANNOUNCEMENTS_ENDPOINT}/organized_announcements`, { params });
  };
}
