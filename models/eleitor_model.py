from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infra.base import Base
from models import pessoa_model
import datetime
import enum

class StatusEnum(str, enum.Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"

class EleitorModel(Base):
    __tablename__ = "eleitores"

    id = Column(Integer, ForeignKey("pessoas.id"), primary_key=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.ATIVO)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    pessoa = relationship("pessoa_model")
