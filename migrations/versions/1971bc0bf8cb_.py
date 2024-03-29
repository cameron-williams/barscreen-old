"""empty message

Revision ID: 1971bc0bf8cb
Revises: c5b71b68c770
Create Date: 2019-04-23 18:54:12.233127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1971bc0bf8cb'
down_revision = 'c5b71b68c770'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('show', 'last_played_clip')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('last_played_clip', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
