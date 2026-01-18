import type { AnnouncementsApiService } from "@shared/services/api/announcements-api-service";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
} from "@shared/services/api/announcements-api-service/types";
import { PaginationService } from "@shared/services/pagination-service";

export class AnnouncementsService {
  paginationService: PaginationService<IAnnouncementDto>;

  constructor(private announcementsApiService: AnnouncementsApiService) {
    const paginationService = new PaginationService<IAnnouncementDto>({
      loadFn: this.announcementsApiService.getAnnouncementList,
    });

    this.paginationService = paginationService;

    paginationService.init();
  }

  createGame = async (params: ICreateAnnouncementDto) => {
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
}
