"""fix device id name issue

Revision ID: dfb5e1d9d41d
Revises: 20e17dd9cd1f
Create Date: 2019-11-28 23:38:42.751225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfb5e1d9d41d'
down_revision = '20e17dd9cd1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_log', sa.Column('device_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.drop_constraint('device_log_device_uuid_fkey', 'device_log', type_='foreignkey')
    op.create_foreign_key(None, 'device_log', 'device', ['device_id'], ['id'], ondelete='CASCADE')
    op.drop_column('device_log', 'device_uuid')
    op.add_column('device_task', sa.Column('device_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'device_task', ['id'])
    op.drop_constraint('device_task_device_uuid_fkey', 'device_task', type_='foreignkey')
    op.create_foreign_key(None, 'device_task', 'device', ['device_id'], ['id'], ondelete='CASCADE')
    op.drop_column('device_task', 'device_uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_task', sa.Column('device_uuid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'device_task', type_='foreignkey')
    op.create_foreign_key('device_task_device_uuid_fkey', 'device_task', 'device', ['device_uuid'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_column('device_task', 'device_id')
    op.add_column('device_log', sa.Column('device_uuid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'device_log', type_='foreignkey')
    op.create_foreign_key('device_log_device_uuid_fkey', 'device_log', 'device', ['device_uuid'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.drop_column('device_log', 'device_id')
    # ### end Alembic commands ###
