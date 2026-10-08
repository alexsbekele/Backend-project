"""add description and created_at to tasks

Revision ID: 530b93c3ffcc
Revises: 8ff6aaea90fc
Create Date: 2026-10-07 23:40:02.898214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '530b93c3ffcc'
down_revision: Union[str, Sequence[str], None] = '8ff6aaea90fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=True),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("completed", sa.Boolean(), server_default=sa.false()),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_tasks_user"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("users")