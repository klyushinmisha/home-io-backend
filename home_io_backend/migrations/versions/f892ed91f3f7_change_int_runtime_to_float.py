"""change int runtime to float

Revision ID: f892ed91f3f7
Revises: c7406e1b7b49
Create Date: 2019-12-18 22:30:14.600790

"""
from alembic import op

revision = 'f892ed91f3f7'
down_revision = 'c7406e1b7b49'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE script ALTER COLUMN runtime TYPE float;')
    op.execute('ALTER TABLE script ALTER COLUMN runtime SET DEFAULT 0;')


def downgrade():
    op.execute('ALTER TABLE script ALTER COLUMN runtime TYPE integer;')
    op.execute('ALTER TABLE script ALTER COLUMN runtime SET DEFAULT 0;')
