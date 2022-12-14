"""empty message

Revision ID: 05e6927bfa66
Revises: fe083a5aec6f
Create Date: 2022-09-19 17:46:30.924493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05e6927bfa66'
down_revision = 'fe083a5aec6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Venue_id', sa.Integer(), nullable=False),
    sa.Column('Artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('website', sa.String(length=200), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=False))
    op.add_column('Venue', sa.Column('seeking_description', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'seeking_description')
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'website')
    op.drop_table('Show')
    # ### end Alembic commands ###
