export enum EAppRoutes {
  Login = "/login",
  Registration = "/registration",
  VerifyEmail = "/verify-email",
  Games = "/games",
  Announcements = "/announcements",
  AccountSettings = "/account-settings",
  MyAnnouncements = "/my-announcements",
}

export enum ERouteParams {
  GameId = "gameId",
  AnnouncementId = "announcementId",
}

export enum EAppSubRoutes {
  ParticipatedAnnouncements = "participated",
  OrganizedAnnouncements = "organized",
  MyRegistrationRequests = "my-requests",
}
