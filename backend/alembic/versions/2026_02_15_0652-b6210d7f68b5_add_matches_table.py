"""Add Matches Table

Revision ID: b6210d7f68b5
Revises: 082de460c6a5
Create Date: 2026-02-15 06:52:52.472149

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6210d7f68b5"
down_revision: Union[str, Sequence[str], None] = "082de460c6a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("announcement_id", sa.Integer(), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("match_number", sa.Integer(), nullable=False),
        sa.Column("participant1_id", sa.Integer(), nullable=True),
        sa.Column("participant2_id", sa.Integer(), nullable=True),
        sa.Column("participant1_score", sa.Integer(), nullable=True),
        sa.Column("participant2_score", sa.Integer(), nullable=True),
        sa.Column("winner_id", sa.Integer(), nullable=True),
        sa.Column("next_match_winner_id", sa.Integer(), nullable=True),
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="PENDING"
        ),
        sa.Column("is_bye", sa.Boolean(), nullable=False),
        sa.Column("is_third_place", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.CheckConstraint(
            "(winner_id IS NULL) OR (winner_id = participant1_id) OR (winner_id = participant2_id)",
            name=op.f("ck_matches_winner_must_be_participant"),
        ),
        sa.ForeignKeyConstraint(
            ["announcement_id"],
            ["announcements.id"],
            name=op.f("fk_matches_announcement_id_announcements"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["next_match_winner_id"],
            ["matches.id"],
            name=op.f("fk_matches_next_match_winner_id_matches"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["participant1_id"],
            ["announcement_participants.id"],
            name=op.f("fk_matches_participant1_id_announcement_participants"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["participant2_id"],
            ["announcement_participants.id"],
            name=op.f("fk_matches_participant2_id_announcement_participants"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["winner_id"],
            ["announcement_participants.id"],
            name=op.f("fk_matches_winner_id_announcement_participants"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_matches")),
        sa.UniqueConstraint(
            "announcement_id",
            "round_number",
            "match_number",
            name="uq_match_position",
        ),
    )
    op.create_index(
        "idx_match_round",
        "matches",
        ["announcement_id", "round_number"],
        unique=False,
    )
    op.create_index(
        op.f("ix_matches_announcement_id"),
        "matches",
        ["announcement_id"],
        unique=False,
    )
    op.create_index(op.f("ix_matches_status"), "matches", ["status"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_matches_status"), table_name="matches")
    op.drop_index(op.f("ix_matches_announcement_id"), table_name="matches")
    op.drop_index("idx_match_round", table_name="matches")
    op.drop_table("matches")
