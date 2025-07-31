"""create grupos_eleitores and grupo_eleitores_eleitores tables

Revision ID: 006
Revises: 005
Create Date: 2025-07-30 18:29:00

"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'grupos_eleitores',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('nome', sa.String, nullable=False, unique=True),
        sa.Column('descricao', sa.String, nullable=False),
        sa.Column('ativo', sa.Boolean, nullable=False, server_default=sa.text('TRUE')),
        sa.Column('data_cadastro', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('nome', name='uq_nome_grupo')
    )

    op.create_table(
        'grupo_eleitores_eleitores',
        sa.Column('grupo_id', sa.Integer, sa.ForeignKey('grupos_eleitores.id'), primary_key=True),
        sa.Column('eleitor_id', sa.Integer, sa.ForeignKey('eleitores.id'), primary_key=True)
    )

def downgrade():
    op.drop_table('grupo_eleitores_eleitores')
    op.drop_table('grupos_eleitores')