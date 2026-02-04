export const REGISTRATION_REQUEST_ENDPOINT = "registration_requests";

export enum ERegistrationRequestStatuses {
  Pending = "pending",
  Approved = "approved",
  Rejected = "rejected",
  Cancelled = "cancelled",
  Expired = "expired",
}

export enum ERegistrationRequestActions {
  Cancel = "cancel",
  Approve = "approve",
  Reject = "reject",
}
