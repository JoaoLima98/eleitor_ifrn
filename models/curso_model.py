from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime


class CursoModel(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String, nullable=False)
    etapa_id = Column(Integer, ForeignKey("etapas.id"), nullable=False)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    etapa = relationship("EtapaModel", back_populates="cursos")
    vinculos = relationship("VinculoModel", back_populates="curso")
