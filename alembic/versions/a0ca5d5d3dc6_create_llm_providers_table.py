"""Create LLM providers table

Revision ID: a0ca5d5d3dc6
Revises: e3d0958fe087
Create Date: 2026-03-24 21:17:58.870985

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column, Integer, String, DateTime, text, PrimaryKeyConstraint
)


# revision identifiers, used by Alembic.
revision: str = "a0ca5d5d3dc6"
down_revision: Union[str, Sequence[str], None] = "e3d0958fe087"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Creates llm_providers table. """

    op.create_table(
        "llm_providers",
        Column("name", String(length=64), nullable=False),
        Column("url", String(length=256), nullable=False),
        Column("port", Integer(), nullable=False),
        Column("description", String(length=256), nullable=True),
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
        PrimaryKeyConstraint("id", name=op.f("pk_llm_providers"))
    )
    op.create_index(
        op.f("ix_llm_providers_id"),
        "llm_providers",
        ["id"],
        unique=False
    )


def downgrade() -> None:
    """ Drop LLM providers table and related indexes."""

    op.drop_index(op.f("ix_llm_providers_id"), table_name="llm_providers")
    op.drop_table("llm_providers")
