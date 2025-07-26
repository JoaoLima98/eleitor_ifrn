from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from infra.base import Base
import datetime

class EtapaModel(Base):
    __tablename__ = "etapas"

    id = Column(Integer, primary_key=True, index=True)
    etapa = Column(Integer, nullable=False)
    turno = Column(String, nullable=False)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    cursos = relationship("CursoModel", back_populates="etapa")

    __table_args__ = (
        # Garante unicidade da combinação etapa + turno
        UniqueConstraint('etapa', 'turno', name='uq_etapa_turno'),
    )
