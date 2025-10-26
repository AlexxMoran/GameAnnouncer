"""add many-to-many relationship to user and announcement

Revision ID: 4ba84043d320
Revises: 91d0b982f45a
Create Date: 2025-10-26 14:53:42.518434

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ba84043d320"
down_revision: Union[str, Sequence[str], None] = "91d0b982f45a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "announcement_participants",
        sa.Column("announcement_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
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
            name=op.f("fk_announcement_participants_announcement_id_announcements"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_announcement_participants_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "announcement_id",
            "user_id",
            name=op.f("pk_announcement_participants"),
        ),
    )
    op.add_column(
        "announcements",
        sa.Column("organizer_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_announcements_organizer_id_users"),
        "announcements",
        "users",
        ["organizer_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("fk_announcements_organizer_id_users"),
        "announcements",
        type_="foreignkey",
    )
    op.drop_column("announcements", "organizer_id")
    op.drop_table("announcement_participants")
    # ### end Alembic commands ###
