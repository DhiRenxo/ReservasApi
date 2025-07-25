"""integracion de nums

Revision ID: 8469c51659a1
Revises: c368405cec56
Create Date: 2025-07-07 18:14:26.057658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = '8469c51659a1'
down_revision: Union[str, None] = 'c368405cec56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aprobaciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reservaid', sa.Integer(), nullable=True),
    sa.Column('aprobadorid', sa.Integer(), nullable=True),
    sa.Column('tipoaprobador', sa.Enum('DOCENTE', 'COORDINADOR', 'SOPORTETI', 'PROGRAMACION', 'ADMINISTRADOR', name='rolusuario'), nullable=True),
    sa.Column('estado', sa.Enum('PENDIENTE', 'APROBADO', 'RECHAZADO', name='estadoaprobacion'), nullable=True),
    sa.Column('fecha_respuesta', sa.DateTime(), nullable=True),
    sa.Column('comentario', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['aprobadorid'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['reservaid'], ['reservas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('aprobacion')
    op.drop_table('sysdiagrams')
    op.alter_column('reservas', 'estado',
               existing_type=sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               type_=sa.Enum('PENDIENTE', 'APROBADA', 'RECHAZADA', name='estadoreserva'),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reservas', 'estado',
               existing_type=sa.Enum('PENDIENTE', 'APROBADA', 'RECHAZADA', name='estadoreserva'),
               type_=sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'),
               existing_nullable=True)
    op.create_table('sysdiagrams',
    sa.Column('name', sa.NVARCHAR(length=128, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('principal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('diagram_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('definition', mssql.VARBINARY(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B617BBCACBA')
    )
    op.create_table('aprobacion',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('reservaid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('aprobadorid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tipoaprobador', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('estado', sa.VARCHAR(length=50, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.Column('fecha_respuesta', sa.DATETIME(), autoincrement=False, nullable=True),
    sa.Column('comentario', sa.VARCHAR(length=255, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['reservaid'], ['reservas.id'], name='FK__aprobacio__reser__3F466844'),
    sa.PrimaryKeyConstraint('id', name='PK__aprobaci__3213E83F27C3963F')
    )
    op.drop_table('aprobaciones')
    # ### end Alembic commands ###
