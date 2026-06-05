"""add type_task to task

Revision ID: b8f2a1c04e3d
Revises: 3df7ddce4b2b
Create Date: 2026-06-05 18:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b8f2a1c04e3d"
down_revision: Union[str, Sequence[str], None] = "3df7ddce4b2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

type_task_enum = sa.Enum("CPU", "MEMORY", "LLM", name="typetask")


def upgrade() -> None:
    type_task_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "task",
        sa.Column(
            "type_task",
            type_task_enum,
            nullable=False,
            server_default="CPU",
        ),
    )
    op.alter_column("task", "type_task", server_default=None)


def downgrade() -> None:
    op.drop_column("task", "type_task")
    type_task_enum.drop(op.get_bind(), checkfirst=True)
