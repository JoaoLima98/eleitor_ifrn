"""create etapas table

Revision ID: 001
Revises: 
Create Date: 2025-07-30 18:20:00

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'etapas',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('etapa', sa.Integer, nullable=False),
        sa.Column('turno', sa.String, nullable=False),
        sa.Column('data_criacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('etapa', 'turno', name='uq_etapa_turno'),
    )

def downgrade():
    op.drop_table('etapas')