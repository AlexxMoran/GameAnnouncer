"""add status and max_participants to announcements

Revision ID: c661da934b30
Revises: 18803b3a5ba0
Create Date: 2026-01-12 15:15:25.446166

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c661da934b30"
down_revision: Union[str, Sequence[str], None] = "18803b3a5ba0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcements",
        sa.Column("status", sa.String(length=50), nullable=False),
    )
    op.add_column(
        "announcements",
        sa.Column("max_participants", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcements", "max_participants")
    op.drop_column("announcements", "status")
