"""init

Revision ID: 424797b6ca14
Revises: None
Create Date: 2016-12-20 11:12:37.865000

"""

# revision identifiers, used by Alembic.
revision = '424797b6ca14'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('weixinhao', sa.Text(), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('sync_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mps_sync_time'), 'mps', ['sync_time'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('image', sa.Text(), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('mp_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mp_id'], ['mps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_timestamp'), 'articles', ['timestamp'], unique=False)
    op.create_table('subscriptions',
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('mp_id', sa.Integer(), nullable=False),
    sa.Column('subscribe_timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['mp_id'], ['mps.id'], ),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('subscriber_id', 'mp_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_articles_timestamp'), table_name='articles')
    op.drop_table('articles')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_mps_sync_time'), table_name='mps')
    op.drop_table('mps')
    ### end Alembic commands ###
