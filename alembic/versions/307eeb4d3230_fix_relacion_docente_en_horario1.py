"""Fix relacion docente en horario1

Revision ID: 307eeb4d3230
Revises: 5ef75a6b15bf
Create Date: 2025-07-09 11:51:03.828523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = '307eeb4d3230'
down_revision: Union[str, None] = '5ef75a6b15bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sysdiagrams')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sysdiagrams',
    sa.Column('name', sa.NVARCHAR(length=128, collation='Modern_Spanish_CI_AS'), autoincrement=False, nullable=False),
    sa.Column('principal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('diagram_id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1), autoincrement=True, nullable=False),
    sa.Column('version', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('definition', mssql.VARBINARY(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B61452AAF60')
    )
    # ### end Alembic commands ###
