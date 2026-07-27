"""add override_motivo to progreso_maestria

Revision ID: h1i2j3k4l5m6
Revises: g1h2i3j4k5l6
Create Date: 2026-07-27 15:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'h1i2j3k4l5m6'
down_revision: Union[str, Sequence[str], None] = 'g1h2i3j4k5l6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columnas_existentes = [col['name'] for col in inspector.get_columns('progreso_maestria')]

    if 'override_motivo' not in columnas_existentes:
        op.add_column(
            'progreso_maestria',
            sa.Column('override_motivo', sa.String(), nullable=True)
        )


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columnas_existentes = [col['name'] for col in inspector.get_columns('progreso_maestria')]

    if 'override_motivo' in columnas_existentes:
        op.drop_column('progreso_maestria', 'override_motivo')
