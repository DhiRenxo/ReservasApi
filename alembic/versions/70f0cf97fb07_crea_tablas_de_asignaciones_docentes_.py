"""crea tablas de asignaciones, docentes, cursos y carreras

Revision ID: 70f0cf97fb07
Revises: f3c978661131
Create Date: 2025-07-25 13:07:07.648524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70f0cf97fb07'
down_revision: Union[str, None] = 'f3c978661131'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('asignacion_docente_curso',
    sa.Column('asignacion_id', sa.Integer(), nullable=False),
    sa.Column('docente_id', sa.Integer(), nullable=False),
    sa.Column('curso_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['asignacion_id'], ['asignacion.id'], ),
    sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], ),
    sa.ForeignKeyConstraint(['docente_id'], ['docentes.id'], ),
    sa.PrimaryKeyConstraint('asignacion_id', 'docente_id', 'curso_id')
    )
    op.add_column('asignacion', sa.Column('estado', sa.Boolean(), nullable=True))
    op.drop_constraint('FK__asignacio__curso__04E4BC85', 'asignacion', type_='foreignkey')
    op.drop_constraint('FK__asignacio__docen__05D8E0BE', 'asignacion', type_='foreignkey')
    op.drop_column('asignacion', 'cursoid')
    op.drop_column('asignacion', 'horas_actuales')
    op.drop_column('asignacion', 'horas_dejara')
    op.drop_column('asignacion', 'observaciones')
    op.drop_column('asignacion', 'horas_totales')
    op.drop_column('asignacion', 'horas_curso')
    op.drop_column('asignacion', 'docenteid')
    op.add_column('docentes', sa.Column('horastemporales', sa.Integer(), nullable=True))
    op.add_column('docentes', sa.Column('horastotales', sa.Integer(), nullable=True))
    op.add_column('docentes', sa.Column('horasdejara', sa.Integer(), nullable=True))
    op.add_column('docentes', sa.Column('observaciones', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('docentes', 'observaciones')
    op.drop_column('docentes', 'horasdejara')
    op.drop_column('docentes', 'horastotales')
    op.drop_column('docentes', 'horastemporales')
    op.add_column('asignacion', sa.Column('docenteid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('asignacion', sa.Column('horas_curso', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('asignacion', sa.Column('horas_totales', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('asignacion', sa.Column('observaciones', sa.VARCHAR(collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True))
    op.add_column('asignacion', sa.Column('horas_dejara', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('asignacion', sa.Column('horas_actuales', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('asignacion', sa.Column('cursoid', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('FK__asignacio__docen__05D8E0BE', 'asignacion', 'docentes', ['docenteid'], ['id'])
    op.create_foreign_key('FK__asignacio__curso__04E4BC85', 'asignacion', 'cursos', ['cursoid'], ['id'])
    op.drop_column('asignacion', 'estado')
    op.drop_table('asignacion_docente_curso')
    # ### end Alembic commands ###
