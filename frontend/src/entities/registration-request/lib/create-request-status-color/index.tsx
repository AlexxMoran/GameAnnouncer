import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";

export const createRequestStatusColor = (status: ERegistrationRequestStatuses) => {
  if (status === ERegistrationRequestStatuses.Approved) return "success";
  if (status === ERegistrationRequestStatuses.Pending) return "warning";
  if (status === ERegistrationRequestStatuses.Rejected) return "error";
  if (status === ERegistrationRequestStatuses.Cancelled) return "error";
  if (status === ERegistrationRequestStatuses.Expired) return "info";
};
