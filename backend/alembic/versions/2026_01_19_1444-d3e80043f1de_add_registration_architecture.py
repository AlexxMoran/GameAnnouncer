"""Add Registration Architecture

Revision ID: d3e80043f1de
Revises: c661da934b30
Create Date: 2026-01-19 14:44:06.602096

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "d3e80043f1de"
down_revision: Union[str, Sequence[str], None] = "c661da934b30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "registration_forms",
        sa.Column("announcement_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["announcement_id"],
            ["announcements.id"],
            name=op.f("fk_registration_forms_announcement_id_announcements"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_registration_forms")),
        sa.UniqueConstraint(
            "announcement_id",
            name=op.f("uq_registration_forms_announcement_id"),
        ),
    )
    op.create_table(
        "form_fields",
        sa.Column("form_id", sa.Integer(), nullable=False),
        sa.Column(
            "field_type",
            sa.String(length=50),
            nullable=False,
            comment="The type of the form field (Example: 'text', 'select', 'checkbox')",
        ),
        sa.Column(
            "label",
            sa.String(length=200),
            nullable=False,
            comment="The label/question for the form field(Example: 'Nickname in Game')",
        ),
        sa.Column(
            "key",
            sa.String(length=100),
            nullable=False,
            comment="The unique key/identifier for store response(Example: 'nickname')",
        ),
        sa.Column(
            "required",
            sa.Boolean(),
            nullable=False,
            comment="Whether this field is required or optional",
        ),
        sa.Column(
            "options",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment="The options for fields like selects, dropdowns or multiple choice",
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["registration_forms.id"],
            name=op.f("fk_form_fields_form_id_registration_forms"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_form_fields")),
        sa.UniqueConstraint("form_id", "key", name="uq_form_fields_form_id_key"),
    )
    op.create_index(
        op.f("ix_form_fields_form_id"),
        "form_fields",
        ["form_id"],
        unique=False,
    )
    op.create_table(
        "form_field_responses",
        sa.Column("registration_request_id", sa.Integer(), nullable=False),
        sa.Column("form_field_id", sa.Integer(), nullable=False),
        sa.Column(
            "value",
            sa.Text(),
            nullable=False,
            comment="The user's response to the form field",
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["form_field_id"],
            ["form_fields.id"],
            name=op.f("fk_form_field_responses_form_field_id_form_fields"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["registration_request_id"],
            ["registration_requests.id"],
            name=op.f(
                "fk_form_field_responses_registration_request_id_registration_requests"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_form_field_responses")),
        sa.UniqueConstraint(
            "registration_request_id",
            "form_field_id",
            name="uq_form_field_responses_registration_request_id_form_field_id",
        ),
    )
    op.create_index(
        op.f("ix_form_field_responses_form_field_id"),
        "form_field_responses",
        ["form_field_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_form_field_responses_registration_request_id"),
        "form_field_responses",
        ["registration_request_id"],
        unique=False,
    )
    op.add_column(
        "registration_requests",
        sa.Column(
            "cancellation_reason",
            sa.Text(),
            nullable=True,
            comment="Reason for cancellation/decline of the registration request",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("registration_requests", "cancellation_reason")
    op.drop_index(
        op.f("ix_form_field_responses_registration_request_id"),
        table_name="form_field_responses",
    )
    op.drop_index(
        op.f("ix_form_field_responses_form_field_id"),
        table_name="form_field_responses",
    )
    op.drop_table("form_field_responses")
    op.drop_index(op.f("ix_form_fields_form_id"), table_name="form_fields")
    op.drop_table("form_fields")
    op.drop_table("registration_forms")
