import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { IUserDto } from "@shared/services/api/auth-api-service/types";
import type {
  ERegistrationRequestActions,
  ERegistrationRequestStatuses,
} from "@shared/services/api/registration-requests-api-service/constants";
import type { IEntityDateFields, IEntityIdField } from "@shared/types/commonEntity.types";
import type { TMaybe } from "@shared/types/main.types";
import type { IPaginationParams } from "@shared/types/pagination.types";

export interface IFormResponse {
  form_field_id: number;
  value: string;
}

export interface IRegistrationRequestDto extends IEntityDateFields, IEntityIdField {
  announcement_id: number;
  announcement: Pick<IAnnouncementDto, "id" | "title" | "game">;
  user: Pick<IUserDto, "id" | "nickname" | "avatar_color" | "avatar_icon_id">;
  status: ERegistrationRequestStatuses;
  cancellation_reason: TMaybe<string>;
}

export interface ICreateRegistrationRequestDto {
  announcement_id: number;
  form_responses?: IFormResponse[];
}

export interface IEditRegistrationRequestDto {
  action: ERegistrationRequestActions;
}

export interface IRegistrationRequestFilters {
  status?: ERegistrationRequestStatuses;
}

export interface IGetRegistrationRequestsDto extends IPaginationParams, IRegistrationRequestFilters {}
