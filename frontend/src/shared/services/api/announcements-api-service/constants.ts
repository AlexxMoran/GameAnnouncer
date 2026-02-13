export const ANNOUNCEMENTS_ENDPOINT = "announcements";

export enum EAnnouncementStatuses {
  PreRegistration = "pre_registration",
  RegistrationOpen = "registration_open",
  RegistrationClosed = "registration_closed",
  Live = "live",
  Paused = "paused",
  Finished = "finished",
  Cancelled = "cancelled",
}

export enum ERegistrationFormFieldTypes {
  Text = "text",
  Select = "select",
  Boolean = "boolean",
}

export enum EAnnouncementFormat {
  SingleElimination = "SINGLE_ELIMINATION",
}
