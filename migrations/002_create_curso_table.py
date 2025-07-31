"""create cursos table

Revision ID: 002
Revises: 001
Create Date: 2025-07-30 18:21:00

"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'cursos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('nome', sa.String, nullable=False, unique=True),
        sa.Column('descricao', sa.String, nullable=False),
        sa.Column('etapa_id', sa.Integer, sa.ForeignKey('etapas.id'), nullable=False),
        sa.Column('data_criacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('cursos')