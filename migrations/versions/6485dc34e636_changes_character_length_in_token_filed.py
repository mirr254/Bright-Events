"""changes character length in token filed

Revision ID: 6485dc34e636
Revises: d5eb2a201a0f
Create Date: 2018-02-07 09:11:01.245420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6485dc34e636'
down_revision = 'd5eb2a201a0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisted_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklisted_tokens')
    # ### end Alembic commands ###