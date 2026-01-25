import type { AnnouncementsApiService } from "@shared/services/api/announcements-api-service";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
  IGetAnnouncementsDto,
} from "@shared/services/api/announcements-api-service/types";
import { PaginationService } from "@shared/services/pagination-service";

// TODO вынести логику крудов в один сервис
export class ParticipatedAnnouncementsService {
  paginationService: PaginationService<IAnnouncementDto, IGetAnnouncementsDto>;

  constructor(private announcementsApiService: AnnouncementsApiService) {
    const paginationService = new PaginationService({
      loadFn: this.announcementsApiService.getParticipatedAnnouncements,
    });

    this.paginationService = paginationService;

    paginationService.init();
  }

  createAnnouncement = async (params: ICreateAnnouncementDto) => {
    try {
      const result = await this.announcementsApiService.createAnnouncement(
        params
      );

      if (result) {
        this.paginationService.init();
      }

      return result;
    } catch (_) {
      /* empty */
    }
  };

  deleteAnnouncement = async (announcementId: number) => {
    try {
      const result = await this.announcementsApiService.deleteAnnouncement(
        announcementId
      );

      if (result) {
        this.paginationService.init();
      }

      return result;
    } catch (_) {
      /* empty */
    }
  };
}
