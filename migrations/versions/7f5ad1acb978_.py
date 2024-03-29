"""empty message

Revision ID: 7f5ad1acb978
Revises: 1317c92c1b76
Create Date: 2019-05-07 15:03:31.246317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7f5ad1acb978'
down_revision = '1317c92c1b76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loop', sa.Column('lp_clips', sa.String(), nullable=True))
    op.drop_column('loop', 'last_played_clips')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loop', sa.Column('last_played_clips', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_column('loop', 'lp_clips')
    # ### end Alembic commands ###
