"""nuevos campos en el modelo User

Revision ID: 7ee82ead7535
Revises: 766e92ed2c59
Create Date: 2018-09-27 17:00:11.518895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ee82ead7535'
down_revision = '766e92ed2c59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'aout_me')
    # ### end Alembic commands ###