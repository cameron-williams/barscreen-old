"""empty message

Revision ID: be8a6b4ff5bc
Revises: 4149e1bce6bc
Create Date: 2019-04-09 20:01:20.978562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be8a6b4ff5bc'
down_revision = '4149e1bce6bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'promo_user_id_fkey', 'promo', type_='foreignkey')
    op.create_foreign_key(None, 'promo', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'promo', type_='foreignkey')
    op.create_foreign_key(u'promo_user_id_fkey', 'promo', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###