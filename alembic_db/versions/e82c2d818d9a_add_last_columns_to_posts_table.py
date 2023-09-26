"""add last columns to posts table

Revision ID: e82c2d818d9a
Revises: 754303967ad6
Create Date: 2023-09-26 19:51:05.773524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e82c2d818d9a'
down_revision: Union[str, None] = '754303967ad6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', column_name='published')
    op.drop_column('posts', column_name='created_at')
