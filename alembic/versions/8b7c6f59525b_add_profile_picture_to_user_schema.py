"""Add profile picture to user schema

Revision ID: 8b7c6f59525b
Revises: 55d31cf846b2
Create Date: 2025-07-13 07:11:31.436310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b7c6f59525b'
down_revision: Union[str, None] = '55d31cf846b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    default_image_url = "https://imgs.search.brave.com/JqLkOW5ls518f8t5iH3rCS376Any3y5s4Jko9jGBHgg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/a2luZHBuZy5jb20v/cGljYy9tLzI0LTI0/ODI1M191c2VyLXBy/b2ZpbGUtZGVmYXVs/dC1pbWFnZS1wbmct/Y2xpcGFydC1wbmct/ZG93bmxvYWQucG5n"
    op.add_column("users", sa.Column("profile_picture", sa.String, nullable=True,
                  comment="URL of the user's profile picture", server_default=default_image_url, default=default_image_url), )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "profile_picture")
