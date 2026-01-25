import { AnnouncementsApiService } from "@shared/services/api/announcements-api-service";
import { AuthApiService } from "@shared/services/api/auth-api-service";
import { BaseApiService } from "@shared/services/api/base-api-service";
import { GamesApiService } from "@shared/services/api/games-api-service";
import { AuthService } from "@shared/services/auth-service";
import type { IRootServiceData } from "@shared/services/root-service/types";

export class RootService {
  // api services
  baseApiService = new BaseApiService();
  gamesApiService = new GamesApiService(this.baseApiService);
  announcementsApiService = new AnnouncementsApiService(this.baseApiService);
  authApiService = new AuthApiService(this.baseApiService);

  authService = new AuthService(this.authApiService);

  constructor(data: IRootServiceData) {
    this.baseApiService.createInterceptors(data, this.authService);
  }
}
