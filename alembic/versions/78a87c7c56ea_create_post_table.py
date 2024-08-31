"""create post table

Revision ID: 78a87c7c56ea
Revises:
Create Date: 2024-08-31 09:56:08.919063

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "78a87c7c56ea"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            primary_key=True,
            index=True,
        ),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
    pass
