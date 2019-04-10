"""empty message

Revision ID: 4149e1bce6bc
Revises: 640d8b64902a
Create Date: 2019-04-09 19:55:26.540708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4149e1bce6bc'
down_revision = '640d8b64902a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('promo', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'promo', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'promo', type_='foreignkey')
    op.drop_column('promo', 'user_id')
    # ### end Alembic commands ###
