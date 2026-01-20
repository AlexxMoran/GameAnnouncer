"""add end_at to announcements

Revision ID: 982afec0add7
Revises: c661da934b30
Create Date: 2026-01-20 16:27:22.481786

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "982afec0add7"
down_revision: Union[str, Sequence[str], None] = "c661da934b30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcements",
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcements", "end_at")
