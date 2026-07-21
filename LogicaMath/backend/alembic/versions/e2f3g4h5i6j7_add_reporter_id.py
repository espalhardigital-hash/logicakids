"""Add reporter_id to ux_feedback

Revision ID: e2f3g4h5i6j7
Revises: f1f2f3f4f5f6
Create Date: 2026-07-21 14:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f3g4h5i6j7'
down_revision = 'f1f2f3f4f5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ux_feedbacks', sa.Column('reporter_id', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_ux_feedbacks_reporter_id'), 'ux_feedbacks', ['reporter_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_ux_feedbacks_reporter_id'), table_name='ux_feedbacks')
    op.drop_column('ux_feedbacks', 'reporter_id')
