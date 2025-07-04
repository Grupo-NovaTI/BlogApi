"""adding created_at and updated-at in TagModel

Revision ID: 55d31cf846b2
Revises: 0aa9f49f159a
Create Date: 2025-07-04 01:05:06.356081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55d31cf846b2'
down_revision: Union[str, None] = '0aa9f49f159a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("tags", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column("tags", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tags", "created_at")
    op.drop_column("tags", "updated_at")
