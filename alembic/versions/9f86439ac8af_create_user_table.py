"""create user table

Revision ID: 9f86439ac8af
Revises: 78a87c7c56ea
Create Date: 2024-08-31 19:27:45.802280

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f86439ac8af"
down_revision: Union[str, None] = "78a87c7c56ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            primary_key=True,
            index=True,
        ),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
