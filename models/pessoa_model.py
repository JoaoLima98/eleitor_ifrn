from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime

class PessoaModel(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    vinculos = relationship("vinculo_model", back_populates="pessoa", cascade="all, delete-orphan")
