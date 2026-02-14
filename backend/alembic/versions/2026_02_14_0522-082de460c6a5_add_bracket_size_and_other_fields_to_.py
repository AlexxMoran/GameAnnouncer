"""Add bracket size and other fields to Announcement

Revision ID: 082de460c6a5
Revises: ef13ddc87c09
Create Date: 2026-02-14 05:22:07.609685

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "082de460c6a5"
down_revision: Union[str, Sequence[str], None] = "ef13ddc87c09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcements",
        sa.Column(
            "has_qualification", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )
    op.add_column("announcements", sa.Column("seed_method", sa.String(), nullable=True))
    op.execute(
        """
        UPDATE announcements
        SET seed_method = 'RANDOM'
        WHERE seed_method IS NULL
        """
    )
    op.alter_column("announcements", "seed_method", nullable=False)

    op.add_column(
        "announcements", sa.Column("bracket_size", sa.Integer(), nullable=True)
    )
    op.add_column(
        "announcements",
        sa.Column(
            "third_place_match", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
    )
    op.add_column(
        "announcements",
        sa.Column(
            "qualification_finished",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcements", "qualification_finished")
    op.drop_column("announcements", "third_place_match")
    op.drop_column("announcements", "bracket_size")
    op.drop_column("announcements", "seed_method")
    op.drop_column("announcements", "has_qualification")
