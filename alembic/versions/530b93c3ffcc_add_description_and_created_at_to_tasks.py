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
    op.create_index("ix_tasks_user_id_created_at", "tasks", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_tasks_user_id_created_at", table_name="tasks")