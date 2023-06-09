"""create templates for money 

Revision ID: cd08d445d07c
Revises: f5d153a21f34
Create Date: 2023-04-25 10:49:32.344310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd08d445d07c'
down_revision = 'f5d153a21f34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('template_money',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('Name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('Value', sa.Integer(), nullable=False),
    sa.Column('Category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Category'], ['category.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('template_money')
    # ### end Alembic commands ###
