"""update and extend Announcement Participant table

Revision ID: c0c1dea4f4f2
Revises: 34d3c70e8734
Create Date: 2026-02-13 09:33:39.188440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c0c1dea4f4f2"
down_revision: Union[str, Sequence[str], None] = "34d3c70e8734"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "announcement_participants",
        sa.Column("qualification_score", sa.Integer(), nullable=True),
    )
    op.add_column(
        "announcement_participants",
        sa.Column("qualification_rank", sa.Integer(), nullable=True),
    )
    op.add_column(
        "announcement_participants",
        sa.Column("seed", sa.Integer(), nullable=True),
    )
    op.add_column(
        "announcement_participants",
        sa.Column(
            "is_qualified", sa.Boolean(), nullable=False, server_default=sa.false()
        ),
    )

    op.drop_constraint(
        "pk_announcement_participants",
        "announcement_participants",
        type_="primary",
    )

    op.add_column(
        "announcement_participants",
        sa.Column("id", sa.Integer(), nullable=True),
    )

    op.execute("CREATE SEQUENCE announcement_participants_id_seq")
    op.execute(
        """
        UPDATE announcement_participants
        SET id = nextval('announcement_participants_id_seq')
        WHERE id IS NULL
        """
    )

    op.alter_column(
        "announcement_participants",
        "id",
        nullable=False,
        server_default=sa.text("nextval('announcement_participants_id_seq')"),
    )
    op.execute(
        "ALTER SEQUENCE announcement_participants_id_seq OWNED BY announcement_participants.id"
    )

    op.create_primary_key(
        "announcement_participants_pkey",
        "announcement_participants",
        ["id"],
    )

    op.create_index(
        "ix_announcement_participant_rank_unique",
        "announcement_participants",
        ["announcement_id", "qualification_rank"],
        unique=True,
        postgresql_where="qualification_rank IS NOT NULL",
    )
    op.create_index(
        "ix_announcement_participant_seed_unique",
        "announcement_participants",
        ["announcement_id", "seed"],
        unique=True,
        postgresql_where="seed IS NOT NULL",
    )
    op.create_index(
        op.f("ix_announcement_participants_announcement_id"),
        "announcement_participants",
        ["announcement_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_announcement_participants_user_id"),
        "announcement_participants",
        ["user_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "uq_announcement_participant_announcement_user",
        "announcement_participants",
        ["announcement_id", "user_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_announcement_participant_announcement_user",
        "announcement_participants",
        type_="unique",
    )
    op.drop_index(
        op.f("ix_announcement_participants_user_id"),
        table_name="announcement_participants",
    )
    op.drop_index(
        op.f("ix_announcement_participants_announcement_id"),
        table_name="announcement_participants",
    )
    op.drop_index(
        "ix_announcement_participant_seed_unique",
        table_name="announcement_participants",
        postgresql_where="seed IS NOT NULL",
    )
    op.drop_index(
        "ix_announcement_participant_rank_unique",
        table_name="announcement_participants",
        postgresql_where="qualification_rank IS NOT NULL",
    )

    op.drop_constraint(
        "announcement_participants_pkey",
        "announcement_participants",
        type_="primary",
    )

    op.drop_column("announcement_participants", "id")
    op.execute("DROP SEQUENCE IF EXISTS announcement_participants_id_seq")

    op.create_primary_key(
        "pk_announcement_participants",
        "announcement_participants",
        ["announcement_id", "user_id"],
    )

    op.drop_column("announcement_participants", "is_qualified")
    op.drop_column("announcement_participants", "seed")
    op.drop_column("announcement_participants", "qualification_rank")
    op.drop_column("announcement_participants", "qualification_score")
