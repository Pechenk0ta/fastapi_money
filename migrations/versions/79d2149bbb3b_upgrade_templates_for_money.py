"""upgrade templates for money 

Revision ID: 79d2149bbb3b
Revises: cd08d445d07c
Create Date: 2023-04-25 11:54:17.246147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79d2149bbb3b'
down_revision = 'cd08d445d07c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_money', sa.Column('name', sa.String(), nullable=False))
    op.add_column('template_money', sa.Column('value', sa.Integer(), nullable=False))
    op.add_column('template_money', sa.Column('category', sa.Integer(), nullable=True))
    op.drop_constraint('template_money_Category_fkey', 'template_money', type_='foreignkey')
    op.create_foreign_key(None, 'template_money', 'category', ['category'], ['id'])
    op.drop_column('template_money', 'Category')
    op.drop_column('template_money', 'Value')
    op.drop_column('template_money', 'Name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('template_money', sa.Column('Name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('template_money', sa.Column('Value', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('template_money', sa.Column('Category', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'template_money', type_='foreignkey')
    op.create_foreign_key('template_money_Category_fkey', 'template_money', 'category', ['Category'], ['id'])
    op.drop_column('template_money', 'category')
    op.drop_column('template_money', 'value')
    op.drop_column('template_money', 'name')
    # ### end Alembic commands ###
