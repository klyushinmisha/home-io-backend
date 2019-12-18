"""add script enable/disable feature

Revision ID: c7406e1b7b49
Revises: 41c2da6857dc
Create Date: 2019-12-18 21:53:58.544585

"""
import sqlalchemy as sa
from alembic import op

revision = 'c7406e1b7b49'
down_revision = '41c2da6857dc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('script', sa.Column('enabled', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('script', 'enabled')
