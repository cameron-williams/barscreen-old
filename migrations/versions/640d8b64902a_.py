"""empty message

Revision ID: 640d8b64902a
Revises: 1ec804d7553f
Create Date: 2019-04-09 18:49:55.013346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '640d8b64902a'
down_revision = '1ec804d7553f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('clip_data', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promo')
    # ### end Alembic commands ###
