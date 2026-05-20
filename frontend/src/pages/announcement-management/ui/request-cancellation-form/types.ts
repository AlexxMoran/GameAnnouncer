import type { ICancellationRequestFields } from "@pages/announcement-management/model/create-cancellation-request-validation-schema/types";
import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";

export interface IRequestCancellationFormProps {
  request: IRegistrationRequestDto;
  onSubmit?: (values: ICancellationRequestFields) => Promise<unknown>;
}
