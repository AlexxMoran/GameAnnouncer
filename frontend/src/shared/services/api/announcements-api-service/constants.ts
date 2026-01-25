export const ANNOUNCEMENTS_ENDPOINT = "announcements";
export const USER_ANNOUNCEMENTS_ENDPOINT = "users/me";

export enum EAnnouncementStatuses {
  PreRegistration = "pre_registration",
  RegistrationOpen = "registration_open",
  RegistrationClosed = "registration_closed",
  Live = "live",
  Paused = "paused",
  Finished = "finished",
  Cancelled = "cancelled",
}
