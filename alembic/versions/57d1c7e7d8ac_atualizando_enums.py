from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    tipovinculo = postgresql.ENUM('DISCENTE', 'DOCENTE', name='tipovinculo')
    tipovinculo.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'vinculos',
        'tipo',
        existing_type=sa.VARCHAR(length=8),
        type_=tipovinculo,
        postgresql_using='tipo::tipovinculo',  # <-- Aqui está o cast explícito
        existing_nullable=False
    )


def downgrade():
    tipovinculo = postgresql.ENUM('DISCENTE', 'DOCENTE', name='tipovinculo')
    
    op.alter_column(
        'vinculos',
        'tipo',
        existing_type=tipovinculo,
        type_=sa.VARCHAR(length=8),
        postgresql_using='tipo::VARCHAR',
        existing_nullable=False
    )

    tipovinculo.drop(op.get_bind(), checkfirst=True)
