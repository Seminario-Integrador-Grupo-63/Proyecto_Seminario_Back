"""Initial Migration

Revision ID: 9fdd7af2aa94
Revises: 
Create Date: 2023-10-07 14:36:55.506567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9fdd7af2aa94'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('waiter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('image', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('restaurant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sidedish',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sa.LargeBinary(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('restaurant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_booked', sa.Boolean(), nullable=False),
    sa.Column('qr_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('restaurant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('restaurant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user')
    )
    op.create_table('dish',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sa.LargeBinary(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('preparation_time', sa.Integer(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('restaurant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('restaurant', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant'], ['restaurant.id'], ),
    sa.ForeignKeyConstraint(['table'], ['table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sidedishoptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish', sa.Integer(), nullable=False),
    sa.Column('side_dish', sa.Integer(), nullable=True),
    sa.Column('extra_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['dish'], ['dish.id'], ),
    sa.ForeignKeyConstraint(['side_dish'], ['sidedish.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orderdetail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish_selected', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('sub_total', sa.Float(), nullable=False),
    sa.Column('customer', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('observation', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['dish_selected'], ['sidedishoptions.id'], ),
    sa.ForeignKeyConstraint(['order'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderdetail')
    op.drop_table('sidedishoptions')
    op.drop_table('order')
    op.drop_table('dish')
    op.drop_table('user')
    op.drop_table('table')
    op.drop_table('sidedish')
    op.drop_table('category')
    op.drop_table('waiter')
    op.drop_table('restaurant')
    # ### end Alembic commands ###
