"""empty message

Revision ID: 1317c92c1b76
Revises: 292ab93fadfd
Create Date: 2019-05-02 10:48:47.089186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1317c92c1b76'
down_revision = '292ab93fadfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_key', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'api_key')
    # ### end Alembic commands ###
