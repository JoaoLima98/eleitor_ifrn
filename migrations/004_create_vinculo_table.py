"""create vinculos table

Revision ID: 004
Revises: 002,003
Create Date: 2025-07-30 18:23:00

"""
from alembic import op
import sqlalchemy as sa

revision = '004'
down_revision = ('002', '003')  # Depende de cursos e pessoas
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'vinculos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tipo', sa.Integer, nullable=False),
        sa.Column('matricula', sa.String, unique=True, nullable=False),
        sa.Column('pessoa_id', sa.Integer, sa.ForeignKey('pessoas.id'), nullable=False),
        sa.Column('curso_id', sa.Integer, sa.ForeignKey('cursos.id'), nullable=False),
        sa.Column('data_criacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('vinculos')