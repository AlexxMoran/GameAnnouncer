import type {
  IEditRegistrationRequestDto,
  IRegistrationRequestDto,
} from "@shared/services/api/registration-requests-api-service/types";
import type { TEntityId } from "@shared/types/commonEntity.types";

export interface IAnnouncementRequestCardProps {
  request: IRegistrationRequestDto;
  changeRequestStatus: (id: TEntityId, params: IEditRegistrationRequestDto) => Promise<unknown>;
}
