"""Add is_published field to blogs model

Revision ID: 0aa9f49f159a
Revises: 
Create Date: 2025-06-22 19:48:00.049287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0aa9f49f159a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name="blogs", column=sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(table_name="blogs", column_name="is_published") 
