"""create moneytx

Revision ID: 23f332a81baf
Revises: d5f747ec567f
Create Date: 2023-04-14 11:55:11.160826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23f332a81baf'
down_revision = 'd5f747ec567f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('money',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(), nullable=True),
    sa.Column('person', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['type'], ['trx_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('money')
    # ### end Alembic commands ###
