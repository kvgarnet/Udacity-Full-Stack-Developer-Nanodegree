"""empty message

Revision ID: ceff7351854a
Revises: d0b3cabe77e1
Create Date: 2022-09-21 15:08:46.426332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceff7351854a'
down_revision = 'd0b3cabe77e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.ARRAY(sa.String(length=130)),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'genres',
               existing_type=sa.ARRAY(sa.String(length=130)),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
    # ### end Alembic commands ###