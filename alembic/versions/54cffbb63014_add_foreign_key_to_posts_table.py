"""add foreign key to posts table

Revision ID: 54cffbb63014
Revises: 757c5a73a4c2
Create Date: 2026-03-25 19:34:58.622144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54cffbb63014'
down_revision: Union[str, Sequence[str], None] = '757c5a73a4c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fk", # name of the foreign key constraint
        source_table = "posts", # source table
        referent_table = "users", # referent table
        local_cols = ["owner_id"], # local columns
        remote_cols = ["id"], # remote columns
        ondelete = "CASCADE" # optional: specify what happens on delete
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "posts_users_fk",
        table_name = "posts",
        type_="foreignkey"
    )
    op.drop_column("posts", "owner_id")
