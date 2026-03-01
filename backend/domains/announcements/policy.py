from core.policies.base_policy import BasePolicy


class AnnouncementPolicy(BasePolicy):
    def can_create(self) -> bool:
        return self.user is not None and self.user.is_active

    def can_edit(self) -> bool:
        return self.is_admin or self.user.id == self.record.organizer_id

    def can_delete(self) -> bool:
        return self.is_admin or self.user.id == self.record.organizer_id

    def can_manage_lifecycle(self) -> bool:
        """
        Permission to fire lifecycle transitions on the announcement.

        Currently equivalent to can_edit. Defined separately to allow future
        divergence (e.g. a co-organizer role that can advance lifecycle but not
        edit metadata).
        """
        return self.is_admin or self.user.id == self.record.organizer_id
