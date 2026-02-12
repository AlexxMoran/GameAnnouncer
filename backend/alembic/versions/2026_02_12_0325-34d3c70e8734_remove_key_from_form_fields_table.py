"""remove key from form fields table

Revision ID: 34d3c70e8734
Revises: c5a29aade580
Create Date: 2026-02-12 03:25:45.225442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "34d3c70e8734"
down_revision: Union[str, Sequence[str], None] = "c5a29aade580"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("uq_form_fields_form_id_key"), "form_fields", type_="unique"
    )
    op.drop_column("form_fields", "key")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "form_fields",
        sa.Column(
            "key",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
            comment="The unique key/identifier for store response(Example: 'nickname')",
        ),
    )
    op.create_unique_constraint(
        op.f("uq_form_fields_form_id_key"),
        "form_fields",
        ["form_id", "key"],
        postgresql_nulls_not_distinct=False,
    )
