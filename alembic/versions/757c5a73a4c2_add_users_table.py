"""Add users table

Revision ID: 757c5a73a4c2
Revises: d16b02df2046
Create Date: 2026-03-25 19:26:11.452658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '757c5a73a4c2'
down_revision: Union[str, Sequence[str], None] = 'd16b02df2046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable = False), # To set the primary key one can also use sa.Column("id", sa.Integer(), nullable = False, primary_key = True)
        sa.Column("email", sa.String(), nullable = False), # To set the unique constraint one can also use sa.Column("email", sa.String(), nullable = False, unique = True)
        sa.Column("password", sa.String(), nullable = False),
        sa.Column("created_at", sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
