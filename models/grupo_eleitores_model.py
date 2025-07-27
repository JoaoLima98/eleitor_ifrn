from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime


class GrupoEleitoresModel(Base):
    __tablename__ = "grupos_eleitores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    eleitores = relationship("EleitorModel", secondary="grupo_eleitores_eleitores", backref="grupos")