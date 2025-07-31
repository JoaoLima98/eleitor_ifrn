"""create pessoas table

Revision ID: 003
Revises: 
Create Date: 2025-07-30 18:22:00

"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'pessoas',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('cpf', sa.String, unique=True, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('data_nascimento', sa.Date, nullable=False),
        sa.Column('data_criacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('data_atualizacao', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade():
    op.drop_table('pessoas')