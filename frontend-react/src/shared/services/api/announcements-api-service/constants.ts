export const ANNOUNCEMENTS_ENDPOINT = "/v1/announcements";

export enum EAnnouncementStatuses {
  PreRegistration = "pre_registration",
  RegistrationOpen = "registration_open",
  RegistrationClosed = "registration_closed",
  Live = "live",
  Paused = "paused",
  Finished = "finished",
  Cancelled = "cancelled",
}
