from enum import Enum


class AnnouncementStatus(str, Enum):
    PRE_REGISTRATION = "pre_registration"
    REGISTRATION_OPEN = "registration_open"
    REGISTRATION_CLOSED = "registration_closed"
    LIVE = "live"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"
