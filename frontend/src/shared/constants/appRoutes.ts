export enum EAppRoutes {
  Login = "/login",
  Registration = "/registration",
  VerifyEmail = "/verify-email",
  Games = "/games",
  Announcements = "/announcements",
  AnnouncementManagement = "/announcements/:id",
  AccountSettings = "/account-settings",
  MyAnnouncements = "/my-announcements",
  RegistrationRequests = "/registration-requests",
}

export enum EMyAnnouncementsTabs {
  Organized = "organized",
  Participated = "participated",
}

export enum EAnnouncementManagementTabs {
  Requests = "requests",
  Qualification = "qualification",
  Broadcast = "broadcast",
  TournamentGrid = "tournament-grid",
}
