"""Create Tables

Revision ID: dff21e78b770
Revises: 
Create Date: 2018-09-13 16:00:40.647717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dff21e78b770'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'character',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(32), nullable=False),
        sa.Column('strength', sa.SmallInteger, nullable=False, default=10),
        sa.Column('intelligence', sa.SmallInteger, nullable=False, default=10),
        sa.Column('wisdom', sa.SmallInteger, nullable=False, default=10),
        sa.Column('dexterity', sa.SmallInteger, nullable=False, default=10),
        sa.Column('constitution', sa.SmallInteger, nullable=False, default=10),
        sa.Column('charisma', sa.SmallInteger, nullable=False, default=10),
        sa.Column('comeliness', sa.SmallInteger, nullable=False, default=10),

        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('user.id'))
    )

    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=False),
    )


def downgrade():
    op.drop_table('character')
    op.drop_table('user')
