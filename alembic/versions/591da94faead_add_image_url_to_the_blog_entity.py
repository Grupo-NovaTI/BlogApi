"""Add image_url to the blog entity

Revision ID: 591da94faead
Revises: 8b7c6f59525b
Create Date: 2025-07-17 04:06:51.501274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '591da94faead'
down_revision: Union[str, None] = '8b7c6f59525b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add image_url column to the blog table
    DEFAULT_BLOG_IMAGE_URL: str = "https://placehold.co/600x400.png?text=Blog+Image"
    op.add_column(
        'blogs',
        sa.Column('image_url', sa.String(), nullable=True, comment="URL of the blog image",
                  default=DEFAULT_BLOG_IMAGE_URL, server_default=DEFAULT_BLOG_IMAGE_URL)
    )

    # Create an index on the image_url column for faster lookups
    op.create_index('ix_blog_image_url', 'blogs', ['image_url'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_blog_image_url', 'blogs')
    op.drop_column('blogs', 'image_url')
