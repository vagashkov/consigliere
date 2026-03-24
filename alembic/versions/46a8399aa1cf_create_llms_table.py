"""Create LLMs table

Revision ID: 46a8399aa1cf
Revises: a0ca5d5d3dc6
Create Date: 2026-03-24 21:37:47.805629

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column, Integer, String, DateTime, text, PrimaryKeyConstraint
)


# revision identifiers, used by Alembic.
revision: str = "46a8399aa1cf"
down_revision: Union[str, Sequence[str], None] = "a0ca5d5d3dc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Creates LLMs table."""

    op.create_table(
        "llms",
        Column("name", String(length=64), nullable=False),
        Column("size", Integer(), nullable=False),
        Column("format", String(length=64), nullable=False),
        Column("parameters", String(length=64), nullable=False),
        Column("quantization_level", String(length=64), nullable=False),
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
        PrimaryKeyConstraint("id", name=op.f("pk_llms"))
    )
    op.create_index(op.f("ix_llms_id"), "llms", ["id"], unique=False)


def downgrade() -> None:
    """ Drops LLMs table and related indexes. """

    op.drop_index(op.f("ix_llms_id"), table_name="llms")
    op.drop_table("llms")
