"""add_partial_unique_index_active_registration_requests

Revision ID: ea2228eec1c2
Revises: 47c8035142dd
Create Date: 2026-03-06 16:40:21.918648

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ea2228eec1c2"
down_revision: Union[str, Sequence[str], None] = "47c8035142dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            "CREATE UNIQUE INDEX ix_registration_requests_active_user_announcement "
            "ON registration_requests (announcement_id, user_id) "
            "WHERE status IN ('PENDING'::registrationstatus, 'APPROVED'::registrationstatus)"
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DROP INDEX IF EXISTS ix_registration_requests_active_user_announcement"
        )
    )
