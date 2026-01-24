"""add dates for announcements

Revision ID: c6e0e0bb5c35
Revises: d7c5f10fd503
Create Date: 2026-01-10 04:23:43.718418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c6e0e0bb5c35"
down_revision: Union[str, Sequence[str], None] = "d7c5f10fd503"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    from datetime import datetime, timezone

    op.add_column(
        "announcements",
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "announcements",
        sa.Column("registration_start_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "announcements",
        sa.Column("registration_end_at", sa.DateTime(timezone=True), nullable=True),
    )

    start_of_year = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    end_of_year = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

    op.execute(
        f"""
        UPDATE announcements
        SET start_at = '{end_of_year}'
        WHERE start_at IS NULL
        """
    )

    op.execute(
        f"""
        UPDATE announcements
        SET registration_start_at = '{start_of_year}'
        WHERE registration_start_at IS NULL
        """
    )

    op.execute(
        f"""
        UPDATE announcements
        SET registration_end_at = '{end_of_year}'
        WHERE registration_end_at IS NULL
        """
    )

    op.alter_column("announcements", "start_at", nullable=False)
    op.alter_column("announcements", "registration_start_at", nullable=False)
    op.alter_column("announcements", "registration_end_at", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcements", "registration_end_at")
    op.drop_column("announcements", "registration_start_at")
    op.drop_column("announcements", "start_at")
