"""add is_active

Revision ID: 679e31579854
Revises: 63673934b0c1
Create Date: 2024-01-23 22:56:16.209365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '679e31579854'
down_revision: Union[str, None] = '63673934b0c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('dish', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('sidedish', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('sidedishoptions', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('table', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('tablesector', sa.Column('is_active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tablesector', 'is_active')
    op.drop_column('table', 'is_active')
    op.drop_column('sidedishoptions', 'is_active')
    op.drop_column('sidedish', 'is_active')
    op.drop_column('dish', 'is_active')
    op.drop_column('category', 'is_active')
    # ### end Alembic commands ###
