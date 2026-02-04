"""merge registration_architecture and end_at branches

Revision ID: c5a29aade580
Revises: d3e80043f1de, 982afec0add7
Create Date: 2026-02-04 14:01:41.079579

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "c5a29aade580"
down_revision: Union[str, Sequence[str], None] = (
    "d3e80043f1de",
    "982afec0add7",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
