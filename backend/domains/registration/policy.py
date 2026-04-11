from core.permissions.base_policy import BasePolicy


class RegistrationRequestPolicy(BasePolicy):
    def can_view(self) -> bool:
        return (
            self.is_admin
            or self.user.id == self.record.user_id
            or self.user.id == self.record.announcement.organizer_id
        )

    def can_approve(self) -> bool:
        return self.is_admin or self.user.id == self.record.announcement.organizer_id

    def can_reject(self) -> bool:
        return self.is_admin or self.user.id == self.record.announcement.organizer_id

    def can_cancel(self) -> bool:
        return self.is_admin or self.user.id == self.record.user_id
