"""add fk, relationship post, users

Revision ID: 81d08cec73ca
Revises: 9f86439ac8af
Create Date: 2024-08-31 19:39:43.363495

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "81d08cec73ca"
down_revision: Union[str, None] = "9f86439ac8af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "owner_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.Boolean,
            server_default="TRUE",
            nullable=False,
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
