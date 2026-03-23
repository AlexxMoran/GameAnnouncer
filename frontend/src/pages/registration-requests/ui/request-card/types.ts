import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";

export interface IRequestCardProps {
  request: IRegistrationRequestDto;
  onCancelRequest?: () => Promise<void>;
}
