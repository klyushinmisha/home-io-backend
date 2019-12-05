"""initial commit

Revision ID: 41c2da6857dc
Revises: 
Create Date: 2019-12-04 18:14:43.858872

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import ArrowType, UUIDType, JSONType

revision = '41c2da6857dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('_password_hash', sa.Binary(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('device',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', UUIDType(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('last_address', sa.String(length=15), nullable=True),
    sa.Column('registered_at', ArrowType(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_id'), 'device', ['id'], unique=False)
    op.create_index(op.f('ix_device_last_address'), 'device', ['last_address'], unique=False)
    op.create_index(op.f('ix_device_name'), 'device', ['name'], unique=False)
    op.create_index(op.f('ix_device_registered_at'), 'device', ['registered_at'], unique=False)
    op.create_index(op.f('ix_device_uuid'), 'device', ['uuid'], unique=True)
    op.create_table('script',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('tag', sa.String(length=64), nullable=False),
    sa.Column('calls', sa.Integer(), nullable=True),
    sa.Column('runtime', sa.Integer(), nullable=True),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('updated_at', ArrowType(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_script_id'), 'script', ['id'], unique=False)
    op.create_table('device_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('log', JSONType(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_device_log_created_at'), 'device_log', ['created_at'], unique=False)
    op.create_table('device_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('task', JSONType(), nullable=False),
    sa.Column('created_at', ArrowType(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['device.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )


def downgrade():
    op.drop_table('device_task')
    op.drop_index(op.f('ix_device_log_created_at'), table_name='device_log')
    op.drop_table('device_log')
    op.drop_index(op.f('ix_script_id'), table_name='script')
    op.drop_table('script')
    op.drop_index(op.f('ix_device_uuid'), table_name='device')
    op.drop_index(op.f('ix_device_registered_at'), table_name='device')
    op.drop_index(op.f('ix_device_name'), table_name='device')
    op.drop_index(op.f('ix_device_last_address'), table_name='device')
    op.drop_index(op.f('ix_device_id'), table_name='device')
    op.drop_table('device')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
