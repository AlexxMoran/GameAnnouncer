"""Add format column for Announcement table

Revision ID: ef13ddc87c09
Revises: c0c1dea4f4f2
Create Date: 2026-02-13 13:35:35.681112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ef13ddc87c09"
down_revision: Union[str, Sequence[str], None] = "c0c1dea4f4f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcements", sa.Column("format", sa.String(length=50), nullable=True)
    )

    op.execute(
        """
        UPDATE announcements
        SET format = 'SINGLE_ELIMINATION'
        WHERE format IS NULL
        """
    )

    op.alter_column("announcements", "format", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcements", "format")
    # ### end Alembic commands ###
