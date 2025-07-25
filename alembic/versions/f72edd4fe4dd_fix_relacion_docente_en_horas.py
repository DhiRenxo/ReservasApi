"""Fix relacion docente en horas

Revision ID: f72edd4fe4dd
Revises: 307eeb4d3230
Create Date: 2025-07-10 18:04:00.066811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = 'f72edd4fe4dd'
down_revision: Union[str, None] = '307eeb4d3230'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sysdiagrams')
    op.add_column('docentes', sa.Column('horassemanal', sa.Integer(), nullable=False))
    op.add_column('docentes', sa.Column('horasactual', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('docentes', 'horasactual')
    op.drop_column('docentes', 'horassemanal')
    op.create_table('sysdiagrams',
    sa.Column('name', sa.NVARCHAR(length=128, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('principal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('diagram_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('definition', mssql.VARBINARY(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B610333EFAA')
    )
    # ### end Alembic commands ###
