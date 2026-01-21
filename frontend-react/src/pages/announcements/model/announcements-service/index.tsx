import type { AnnouncementsApiService } from "@shared/services/api/announcements-api-service";
import type {
  IAnnouncementDto,
  ICreateAnnouncementDto,
  IGetAnnouncementListDto,
} from "@shared/services/api/announcements-api-service/types";
import { PaginationService } from "@shared/services/pagination-service";

export class AnnouncementsService {
  paginationService: PaginationService<
    IAnnouncementDto,
    IGetAnnouncementListDto
  >;

  constructor(private announcementsApiService: AnnouncementsApiService) {
    const paginationService = new PaginationService({
      loadFn: this.announcementsApiService.getAnnouncementList,
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
