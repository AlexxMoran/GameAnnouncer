from core.permissions.base_policy import BasePolicy


class GamePolicy(BasePolicy):
    def can_view(self) -> bool:
        """Games are public catalog data; anyone may view them."""
        return True

    def can_create(self) -> bool:
        return self.is_admin

    def can_edit(self) -> bool:
        return self.is_admin

    def can_delete(self) -> bool:
        return self.is_admin
