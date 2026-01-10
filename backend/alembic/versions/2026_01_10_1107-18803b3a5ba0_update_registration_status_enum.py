"""update registration status enum

Revision ID: 18803b3a5ba0
Revises: c6e0e0bb5c35
Create Date: 2026-01-10 11:07:22.334133

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "18803b3a5ba0"
down_revision: Union[str, Sequence[str], None] = "c6e0e0bb5c35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE registrationstatus ADD VALUE IF NOT EXISTS 'EXPIRED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
