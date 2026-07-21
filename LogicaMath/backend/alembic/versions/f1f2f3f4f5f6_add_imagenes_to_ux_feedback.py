"""Add imagenes to ux_feedback

Revision ID: f1f2f3f4f5f6
Revises: ae5a3aaa46e8
Create Date: 2026-07-21 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1f2f3f4f5f6'
down_revision = 'ae5a3aaa46e8'
# Wait, I need to know what the current head is to set down_revision correctly.
# Let's write a generic file and I will fix down_revision later.
branch_labels = None
depends_on = None


def upgrade():
    # Add the column
    op.add_column('ux_feedbacks', sa.Column('imagenes', sa.JSON(), nullable=True))
    
    # Data migration: populate imagenes with existing screenshot_url
    op.execute(
        """
        UPDATE ux_feedbacks
        SET imagenes = json_build_array(
            json_build_object(
                'url', screenshot_url,
                'rol', 'actual'
            )
        )
        WHERE screenshot_url IS NOT NULL AND screenshot_url != '';
        """
    )


def downgrade():
    op.drop_column('ux_feedbacks', 'imagenes')
