from enum import Enum


class RegistrationStatus(str, Enum):
    """Status of registration request for tournament announcement"""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
