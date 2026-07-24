"""add_tjs_columns_to_configuracion_progreso

Agrega las tres columnas del Modelo B (TJS) a configuracion_progreso:
  - errores_tolerados         : INTEGER, NULL por defecto (Decisión 8)
  - pistas_permitidas         : INTEGER, NOT NULL DEFAULT 0 (Decisión 14)
  - penalizacion_pista_segundos: INTEGER, NOT NULL DEFAULT 0 (Decisión 14)

Los defaults garantizan retrocompatibilidad total con Fases 1–3 (Modelo A):
  - errores_tolerados = NULL  → el backend sigue usando el cálculo heredado
    por porcentaje (comportamiento legacy). Solo las Fases 4–11 lo fijan
    explícito (Decisión 8 y §4.1.1 del macro).
  - pistas_permitidas = 0     → sin pistas, idéntico al comportamiento actual.
  - penalizacion_pista_segundos = 0 → sin penalización, idéntico al actual.

Ref: docs/reestructuraciondefases.md §12.6 y Decisiones 8 y 14.

Revision ID: g1h2i3j4k5l6
Revises: f1f2f3f4f5f6
Create Date: 2026-07-24 02:38:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'g1h2i3j4k5l6'
down_revision: Union[str, Sequence[str], None] = 'e2f3g4h5i6j7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Añade tres columnas a configuracion_progreso (schema-only, sin siembra de datos).

    Seguridad ante re-ejecución parcial: se inspecciona la tabla antes de
    intentar agregar cada columna, igual que la convención del proyecto
    (ver a1b2c3d4e5f9_add_aprobado_por_admin.py).
    """
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columnas_existentes = [col['name'] for col in inspector.get_columns('configuracion_progreso')]

    # 1. errores_tolerados — INTEGER, NULL por defecto (Decisión 8)
    #    NULL en filas antiguas → comportamiento legacy por porcentaje (Fases 1–3).
    #    Las filas de Fases 4–11 lo fijan explícito en el seed posterior.
    if 'errores_tolerados' not in columnas_existentes:
        op.add_column(
            'configuracion_progreso',
            sa.Column('errores_tolerados', sa.Integer(), nullable=True)
        )

    # 2. pistas_permitidas — INTEGER, NOT NULL DEFAULT 0 (Decisión 14)
    #    0 = sin pistas; comportamiento idéntico al actual para Fases 1–3.
    if 'pistas_permitidas' not in columnas_existentes:
        op.add_column(
            'configuracion_progreso',
            sa.Column(
                'pistas_permitidas',
                sa.Integer(),
                nullable=False,
                server_default='0'
            )
        )

    # 3. penalizacion_pista_segundos — INTEGER, NOT NULL DEFAULT 0 (Decisión 14)
    #    0 = sin penalización; comportamiento idéntico al actual para Fases 1–3.
    if 'penalizacion_pista_segundos' not in columnas_existentes:
        op.add_column(
            'configuracion_progreso',
            sa.Column(
                'penalizacion_pista_segundos',
                sa.Integer(),
                nullable=False,
                server_default='0'
            )
        )


def downgrade() -> None:
    """
    Elimina las tres columnas TJS de configuracion_progreso.

    Igual que upgrade: se inspecciona antes de intentar el DROP.
    """
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columnas_existentes = [col['name'] for col in inspector.get_columns('configuracion_progreso')]

    if 'penalizacion_pista_segundos' in columnas_existentes:
        op.drop_column('configuracion_progreso', 'penalizacion_pista_segundos')

    if 'pistas_permitidas' in columnas_existentes:
        op.drop_column('configuracion_progreso', 'pistas_permitidas')

    if 'errores_tolerados' in columnas_existentes:
        op.drop_column('configuracion_progreso', 'errores_tolerados')
