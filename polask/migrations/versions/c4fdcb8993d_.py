"""empty message

Revision ID: c4fdcb8993d
Revises: 456360784951
Create Date: 2014-09-20 20:16:37.177309

"""

# revision identifiers, used by Alembic.
revision = 'c4fdcb8993d'
down_revision = '456360784951'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['email'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user')
    ### end Alembic commands ###
