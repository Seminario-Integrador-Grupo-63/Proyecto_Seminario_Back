"""add number to table

Revision ID: 63673934b0c1
Revises: 8d12a802543e
Create Date: 2024-01-07 22:42:50.415473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '63673934b0c1'
down_revision: Union[str, None] = '8d12a802543e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('table', sa.Column('number', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('table', 'number')
    # ### end Alembic commands ###
