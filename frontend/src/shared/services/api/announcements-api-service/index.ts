import { ANNOUNCEMENTS_ENDPOINT } from "@shared/services/api/announcements-api-service/constants";
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
import { USERS_ME_ENDPOINT } from "@shared/services/api/constants";
import type { IPaginationMeta } from "@shared/types/pagination.types";

export class AnnouncementsApiService {
  constructor(private baseApiService: BaseApiService) {}

  getAnnouncement = (id: number) =>
    this.baseApiService.get<TApiResponseWrapper<IAnnouncementDto>>(`/v1/${ANNOUNCEMENTS_ENDPOINT}/${id}`);

  getAnnouncements = (params: IGetAnnouncementsDto) =>
    this.baseApiService.get<TApiResponseWrapper<IAnnouncementDto[]>, IPaginationMeta>(`/v1/${ANNOUNCEMENTS_ENDPOINT}`, {
      params,
    });

  createAnnouncement = (params: ICreateAnnouncementDto) =>
    this.baseApiService.post<TApiResponseWrapper<IAnnouncementDto>>(`/v1/${ANNOUNCEMENTS_ENDPOINT}`, params);

  editAnnouncement = (id: number, params: IEditAnnouncementDto) =>
    this.baseApiService.patch<TApiResponseWrapper<IAnnouncementDto>>(`/v1/${ANNOUNCEMENTS_ENDPOINT}/${id}`, params);

  deleteAnnouncement = (id: number) =>
    this.baseApiService.delete<TApiResponseWrapper<IAnnouncementDto>>(`/v1/${ANNOUNCEMENTS_ENDPOINT}/${id}`);

  getParticipatedAnnouncements = (params: IGetParticipatedAnnouncementsDto) =>
    this.baseApiService.get<TApiResponseWrapper<IAnnouncementDto[]>, IPaginationMeta>(
      `/v1/${USERS_ME_ENDPOINT}/participated_announcements`,
      {
        params,
      }
    );

  getOrganizedAnnouncements = (params: IGetOrganizedAnnouncementsDto) =>
    this.baseApiService.get<TApiResponseWrapper<IAnnouncementDto[]>, IPaginationMeta>(
      `/v1/${USERS_ME_ENDPOINT}/organized_announcements`,
      { params }
    );
}
