from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ForeignKey, Enum, Date, Boolean, Table
import enum
from sqlalchemy.orm import relationship, declarative_base
from infra.base import Base
import datetime

Base = declarative_base()

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


class CursoModel(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String, nullable=False)
    
    # Foreign key para EtapaModel.id
    etapa_id = Column(Integer, ForeignKey("etapas.id"), nullable=False)
    
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relacionamento com etapa para carregar objeto EtapaModel
    etapa = relationship("EtapaModel", back_populates="cursos")
    vinculos = relationship("VinculoModel", back_populates="curso")

class PessoaModel(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    vinculos = relationship("VinculoModel", back_populates="pessoa", cascade="all, delete-orphan")

class TipoVinculo(int, enum.Enum):
    DISCENTE = 1
    DOCENTE = 2

class VinculoModel(Base):
    __tablename__ = "vinculos"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, nullable=False)
    tipo = Column(Enum(TipoVinculo, native_enum=False), nullable=False)
    pessoa_id = Column(Integer, ForeignKey("pessoas.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="SET NULL"), nullable=True)

    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    pessoa = relationship("PessoaModel", back_populates="vinculos")
    curso = relationship("CursoModel", back_populates="vinculos")


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

    pessoa = relationship("PessoaModel")

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
