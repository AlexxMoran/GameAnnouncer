from core.policies.base_policy import BasePolicy


class RegistrationRequestPolicy(BasePolicy):
    def can_view(self):
        return (
            self.is_admin
            or self.user.id == self.record.user_id
            or self.user.id == self.record.announcement.organizer_id
        )

    def can_approve(self):
        return self.is_admin or self.user.id == self.record.announcement.organizer_id

    def can_reject(self):
        return self.is_admin or self.user.id == self.record.announcement.organizer_id

    def can_cancel(self):
        return self.is_admin or self.user.id == self.record.user_id
