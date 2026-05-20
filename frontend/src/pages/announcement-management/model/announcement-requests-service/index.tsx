import type { RegistrationRequestsApiService } from "@shared/services/api/registration-requests-api-service";
import type {
  IEditRegistrationRequestDto,
  IGetRegistrationRequestsDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";

export class AnnouncementRequestsService extends EntityCrudService<
  IRegistrationRequestDto,
  IGetRegistrationRequestsDto,
  never,
  IEditRegistrationRequestDto
> {
  constructor(registrationRequestsApiService: RegistrationRequestsApiService, announcementId: number) {
    super({
      getEntitiesFn: (params) => registrationRequestsApiService.getAnnouncementRequests(announcementId, params),
      editEntityFn: registrationRequestsApiService.editRegistrationRequest,
      hasFiltersReaction: true,
    });
  }
}
