"""table state

Revision ID: 8d12a802543e
Revises: 866d73ee9210
Create Date: 2023-11-01 23:20:38.861720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8d12a802543e'
down_revision: Union[str, None] = '866d73ee9210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    tablestate = postgresql.ENUM('free', 'occupied', 'waiting', 'payment_ready', name='tablestate', create_type=False)
    tablestate.create(op.get_bind(), checkfirst=True)
    op.add_column('table', sa.Column('state', tablestate, nullable=True))

    op.alter_column('table', 'restaurant',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('table', 'is_booked')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('table', sa.Column('is_booked', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.alter_column('table', 'restaurant',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('table', 'state')
    # ### end Alembic commands ###
