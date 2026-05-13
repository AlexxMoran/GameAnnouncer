import type { AnnouncementsApiService } from "@shared/services/api/announcements-api-service";
import type { IAnnouncementDto, IEditAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { AuthService } from "@shared/services/auth-service";
import type { TMaybe } from "@shared/types/main.types";
import isUndefined from "lodash/isUndefined";
import { makeAutoObservable, runInAction } from "mobx";

export class AnnouncementManagementService {
  announcement: TMaybe<IAnnouncementDto> = null;
  isLoading = false;

  constructor(
    private announcementsApiService: AnnouncementsApiService,
    private authService: AuthService,
    private routeId?: string
  ) {
    makeAutoObservable(this);

    this.getAnnouncement();

    this.cancelAnnouncement = this.cancelAnnouncement.bind(this);
    this.startAnnouncement = this.startAnnouncement.bind(this);
    this.editAnnouncement = this.editAnnouncement.bind(this);
  }

  get isOrganizer() {
    const meId = this.authService.me?.id;
    const organizerId = this.announcement?.organizer_id;

    return !isUndefined(meId) && !isUndefined(organizerId) && meId === organizerId;
  }

  get hasQualification() {
    return this.announcement?.has_qualification;
  }

  get announcementId() {
    if (this.routeId && !isNaN(+this.routeId)) {
      return +this.routeId;
    }
  }

  async getAnnouncement() {
    if (this.announcementId) {
      this.isLoading = true;

      try {
        const { data } = await this.announcementsApiService.getAnnouncement(this.announcementId);

        runInAction(() => {
          this.announcement = data.data;
          this.isLoading = false;
        });
      } catch (_) {
        /* empty */
      }
    }
  }

  async cancelAnnouncement() {
    if (this.announcementId) {
      try {
        const { data } = await this.announcementsApiService.cancelAnnouncement(this.announcementId);

        runInAction(() => {
          this.announcement = data.data;
        });

        return data;
      } catch (_) {
        /* empty */
      }
    }
  }

  async startAnnouncement() {
    if (this.announcementId) {
      try {
        const { data } = this.hasQualification
          ? await this.announcementsApiService.startAnnouncementQualification(this.announcementId)
          : await this.announcementsApiService.generateAnnouncementBracket(this.announcementId);

        runInAction(() => {
          this.announcement = data.data;
        });

        return data;
      } catch (_) {
        /* empty */
      }
    }
  }

  async editAnnouncement(params: IEditAnnouncementDto) {
    if (this.announcementId) {
      try {
        const { data } = await this.announcementsApiService.editAnnouncement(this.announcementId, params);

        runInAction(() => {
          this.announcement = data.data;
        });

        return data;
      } catch (_) {
        /* empty */
      }
    }
  }
}
