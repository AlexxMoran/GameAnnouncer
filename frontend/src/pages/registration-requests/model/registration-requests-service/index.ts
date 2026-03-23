import type { RegistrationRequestsApiService } from "@shared/services/api/registration-requests-api-service";
import type {
  IEditRegistrationRequestDto,
  IGetRegistrationRequestsDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";

export class RegistrationRequestsService extends EntityCrudService<
  IRegistrationRequestDto,
  IGetRegistrationRequestsDto,
  never,
  IEditRegistrationRequestDto
> {
  constructor(registrationRequestsApiService: RegistrationRequestsApiService) {
    super({
      getEntitiesFn: registrationRequestsApiService.getMyRequests,
      editEntityFn: registrationRequestsApiService.editRegistrationRequest,
    });
  }
}
