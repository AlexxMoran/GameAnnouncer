import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";

export interface IRequestCardProps {
  request: IRegistrationRequestDto;
  actionList?: IMenuAction[];
}
