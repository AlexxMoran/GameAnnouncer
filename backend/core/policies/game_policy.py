from core.policies.base_policy import BasePolicy


class GamePolicy(BasePolicy):
    def can_create(self):
        return self.is_admin

    def can_edit(self):
        return self.is_admin

    def can_delete(self):
        return self.is_admin
