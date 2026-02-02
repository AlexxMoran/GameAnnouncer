import type {
  ERegistrationRequestActions,
  ERegistrationRequestStatuses,
} from "@shared/services/api/registration-requests-api-service/constants";
import type { IEntityDateFields, IEntityIdField } from "@shared/types/commonEntity.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export interface IRegistrationRequestDto extends IEntityDateFields, IEntityIdField {
  announcement_id: number;
  user_id: number;
  status: ERegistrationRequestStatuses;
}

export interface ICreateRegistrationRequestDto {
  announcement_id: number;
}

export interface IEditRegistrationRequestDto {
  action: ERegistrationRequestActions;
}

export interface IGetRegistrationRequestsDto extends IPaginationParams {}
