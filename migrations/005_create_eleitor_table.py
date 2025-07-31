"""create eleitores table

Revision ID: 002
Revises: 001
Create Date: 2025-07-30 18:13:00

"""

from alembic import op
import sqlalchemy as sa
import enum

revision = '005'
down_revision = '003'  # Depende apenas de pessoas
branch_labels = None
depends_on = None

class StatusEnum(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"

def upgrade():
    op.create_table(
        'eleitores',
        sa.Column('id', sa.Integer, sa.ForeignKey('pessoas.id'), primary_key=True),
        sa.Column('status', sa.Enum(StatusEnum, name="statusenum"), nullable=False, server_default="ATIVO"),
        sa.Column('data_criacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('eleitores')
    op.execute('DROP TYPE IF EXISTS statusenum')