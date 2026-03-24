"""Create user profiles table

Revision ID: e3d0958fe087
Revises: 065f53831dd2
Create Date: 2026-03-24 21:12:29.641537

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column, Integer, String, DateTime, text,
    ForeignKeyConstraint, PrimaryKeyConstraint
)


# revision identifiers, used by Alembic.
revision: str = "e3d0958fe087"
down_revision: Union[str, Sequence[str], None] = "065f53831dd2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Create user profiles table. """

    op.create_table(
        "user_profiles",
        Column("user", Integer(), nullable=False),
        Column("first_name", String(length=64), nullable=False),
        Column("last_name", String(length=64), nullable=False),
        Column("id", Integer(), autoincrement=True, nullable=False),
        Column(
            "created_at",
            DateTime(timezone=True),
            server_default=text("now()"),
            nullable=False
        ),
        Column(
            "updated_at",
            DateTime(timezone=True),
            server_default=text("now()"),
            nullable=False
        ),
        ForeignKeyConstraint(
            ["user"],
            ["users.id"],
            name=op.f("fk_user_profiles_user_users")
        ),
        PrimaryKeyConstraint(
            "id",
            name=op.f("pk_user_profiles")
        )
    )
    op.create_index(op.f("ix_user_profiles_id"), "user_profiles", ["id"], unique=False)


def downgrade() -> None:
    """ Drops user profile table and related index(es). """

    op.drop_index(op.f("ix_user_profiles_id"), table_name="user_profiles")
    op.drop_table("user_profiles")
