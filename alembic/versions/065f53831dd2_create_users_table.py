"""Create users table

Revision ID: 065f53831dd2
Revises: 
Create Date: 2026-03-24 21:07:12.649176

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Enum,
    PrimaryKeyConstraint, UniqueConstraint, text
)


# revision identifiers, used by Alembic.
revision: str = "065f53831dd2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Create users table. """

    op.create_table(
        "users",
        Column("email", String(length=64), nullable=False),
        Column("password_hash", String(length=128), nullable=False),
        Column("is_active", Boolean(), nullable=False),
        Column(
            "role",
            Enum("ADMIN", "STAFF", "USER", name="userrole"),
            nullable=False
        ),
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
        PrimaryKeyConstraint("id", name=op.f("pk_users")),
        UniqueConstraint("email", name=op.f("uq_users_email"))
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    """ Drop users table and related indexes. """

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
