"""ammount -> amount

Revision ID: 866d73ee9210
Revises: 9f567511f855
Create Date: 2023-10-27 23:07:12.267726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '866d73ee9210'
down_revision: Union[str, None] = '9f567511f855'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orderdetail', sa.Column('amount', sa.Integer(), nullable=False))
    op.drop_column('orderdetail', 'ammount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orderdetail', sa.Column('ammount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('orderdetail', 'amount')
    # ### end Alembic commands ###
