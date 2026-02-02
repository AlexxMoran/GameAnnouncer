import type { BaseApiService } from "@shared/services/api/base-api-service";
import type { TApiResponseWrapper } from "@shared/services/api/base-api-service/types";
import { USERS_ME_ENDPOINT } from "@shared/services/api/constants";
import { REGISTRATION_REQUEST_ENDPOINT } from "@shared/services/api/registration-requests-api-service/constants";
import type {
  ICreateRegistrationRequestDto,
  IEditRegistrationRequestDto,
  IGetRegistrationRequestsDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import type { IPaginationMeta } from "@shared/types/pagination.types";

export class RegistrationRequestsApiService {
  constructor(private baseApiService: BaseApiService) {}

  getMyRequests = (params?: IGetRegistrationRequestsDto) =>
    this.baseApiService.get<TApiResponseWrapper<IRegistrationRequestDto[]>, IPaginationMeta>(
      `v1/${USERS_ME_ENDPOINT}/registration_requests`,
      {
        params,
      }
    );

  createRegistrationRequest = (params: ICreateRegistrationRequestDto) =>
    this.baseApiService.post<TApiResponseWrapper<IRegistrationRequestDto>>(
      `v1/${REGISTRATION_REQUEST_ENDPOINT}`,
      params
    );

  editRegistrationRequest = (id: number, { action }: IEditRegistrationRequestDto) =>
    this.baseApiService.patch<TApiResponseWrapper<IRegistrationRequestDto>>(
      `v1/${REGISTRATION_REQUEST_ENDPOINT}/${id}/${action}`,
      {}
    );
}
