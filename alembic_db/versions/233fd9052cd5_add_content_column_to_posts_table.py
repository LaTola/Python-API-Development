"""add content column to posts table

Revision ID: 233fd9052cd5
Revises: dfb072c306ab
Create Date: 2023-09-26 18:51:36.281356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '233fd9052cd5'
down_revision: Union[str, None] = 'dfb072c306ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
