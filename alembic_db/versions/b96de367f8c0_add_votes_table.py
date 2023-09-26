"""add votes table

Revision ID: b96de367f8c0
Revises: e82c2d818d9a
Create Date: 2023-09-26 20:38:07.304722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b96de367f8c0'
down_revision: Union[str, None] = 'e82c2d818d9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('post_id', sa.Integer, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id'))


def downgrade() -> None:
    op.drop_table('votes')
