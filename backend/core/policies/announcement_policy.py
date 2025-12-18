from core.policies.base_policy import BasePolicy


class AnnouncementPolicy(BasePolicy):
    def can_create(self):
        return self.user is not None and self.user.is_active

    def can_edit(self):
        return self.is_admin or self.user.id == self.record.organizer_id

    def can_delete(self):
        return self.is_admin or self.user.id == self.record.organizer_id
