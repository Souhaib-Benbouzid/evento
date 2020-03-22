"""empty message

Revision ID: d261c771e7e4
Revises: 
Create Date: 2020-03-22 13:50:14.901415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd261c771e7e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('party',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('state', sa.String(length=60), nullable=False),
    sa.Column('city', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('person_event',
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('party_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['party_id'], ['party.id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.UniqueConstraint('party_id'),
    sa.UniqueConstraint('person_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person_event')
    op.drop_table('person')
    op.drop_table('party')
    # ### end Alembic commands ###