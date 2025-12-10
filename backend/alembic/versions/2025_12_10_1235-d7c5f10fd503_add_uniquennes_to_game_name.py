"""add uniquennes to game name

Revision ID: d7c5f10fd503
Revises: 0462102118a4
Create Date: 2025-12-10 12:35:25.153414

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d7c5f10fd503"
down_revision: Union[str, Sequence[str], None] = "0462102118a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(op.f("uq_games_name"), "games", ["name"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("uq_games_name"), "games", type_="unique")
