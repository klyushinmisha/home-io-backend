'''remove src_path from script

Revision ID: 7817eb50b0c1
Revises: 3f7a7675c03a
Create Date: 2019-11-14 07:59:53.398229

'''
import sqlalchemy as sa
from alembic import op

revision = '7817eb50b0c1'
down_revision = '3f7a7675c03a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'device', ['uuid'])
    op.create_unique_constraint(None, 'device_log', ['id'])
    op.create_unique_constraint(None, 'device_task', ['id'])
    op.drop_column('script', 'src_path')


def downgrade():
    op.add_column('script', sa.Column('src_path', sa.VARCHAR(length=4096), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'device_task', type_='unique')
    op.drop_constraint(None, 'device_log', type_='unique')
    op.drop_constraint(None, 'device', type_='unique')
