from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime

# Tabela associativa entre grupo e eleitor
grupo_eleitores_associacao = Table(
    "grupo_eleitores_eleitores",
    Base.metadata,
    Column("grupo_id", Integer, ForeignKey("grupos_eleitores.id"), primary_key=True),
    Column("eleitor_id", Integer, ForeignKey("eleitores.id"), primary_key=True)
)

class GrupoEleitoresModel(Base):
    __tablename__ = "grupos_eleitores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)

    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    eleitores = relationship("EleitorModel", secondary=grupo_eleitores_associacao, backref="grupos")

    __table_args__ = (
        UniqueConstraint('nome', name='uq_nome_grupo'),
    )
