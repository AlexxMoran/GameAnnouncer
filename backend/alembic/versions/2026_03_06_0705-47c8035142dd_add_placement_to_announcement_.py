"""add placement to announcement participants

Revision ID: 47c8035142dd
Revises: b6210d7f68b5
Create Date: 2026-03-06 07:05:33.576936

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "47c8035142dd"
down_revision: Union[str, Sequence[str], None] = "b6210d7f68b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcement_participants",
        sa.Column("placement", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("announcement_participants", "placement")
