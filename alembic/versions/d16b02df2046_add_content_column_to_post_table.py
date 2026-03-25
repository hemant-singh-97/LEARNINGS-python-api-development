"""add content column to post table

Revision ID: d16b02df2046
Revises: 70c53f4f1d9d
Create Date: 2026-03-25 19:18:54.520397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd16b02df2046'
down_revision: Union[str, Sequence[str], None] = '70c53f4f1d9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
