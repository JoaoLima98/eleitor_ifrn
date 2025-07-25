from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime

class VinculoModel(Base):
    __tablename__ = "vinculos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    pessoa_id = Column(Integer, ForeignKey("pessoas.id"), nullable=False)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    pessoa = relationship("PessoaModel", back_populates="vinculos")
