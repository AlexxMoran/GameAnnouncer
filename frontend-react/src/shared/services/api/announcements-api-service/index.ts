import { ANNOUNCEMENTS_ENDPOINT } from "@shared/services/api/announcements-api-service/constants";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
  IEditAnnouncementDto,
  IGetAnnouncementListDto,
} from "@shared/services/api/announcements-api-service/types";
import type { BaseApiService } from "@shared/services/api/base-api-service";
import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import type { IPaginationMeta } from "@shared/types/pagination.types";

export class AnnouncementsApiService {
  constructor(private baseApiService: BaseApiService) {}

  getAnnouncementList = (params: IGetAnnouncementListDto) => {
    return this.baseApiService.get<
      TApiResponseWrapper<IAnnouncementDto[]>,
      IPaginationMeta
    >(ANNOUNCEMENTS_ENDPOINT, { params });
  };

  createAnnouncement = (params: ICreateAnnouncementDto) => {
    return this.baseApiService.post<TApiResponseWrapper<IAnnouncementDto>>(
      ANNOUNCEMENTS_ENDPOINT,
      params
    );
  };

  editAnnouncement = (id: number, params: IEditAnnouncementDto) => {
    return this.baseApiService.patch<TApiResponseWrapper<IAnnouncementDto>>(
      `${ANNOUNCEMENTS_ENDPOINT}/${id}`,
      params
    );
  };

  deleteAnnouncement = (id: number) => {
    return this.baseApiService.delete<TApiResponseWrapper<IAnnouncementDto>>(
      `${ANNOUNCEMENTS_ENDPOINT}/${id}`
    );
  };
}
