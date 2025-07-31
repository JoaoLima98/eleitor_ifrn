from domain.pessoa import Pessoa
from sqlalchemy import select
from sqlalchemy.orm import Session
from infra.db import SessionLocal
from models import models

class PessoaRepository:
    def salvar(self, pessoa):
        # Converte os vínculos do domínio para os modelos ORM
        vinculos_orm = [
            models.VinculoModel(
                id=vinculo.id,
                tipo=vinculo.tipo.value if hasattr(vinculo.tipo, "value") else vinculo.tipo,
                pessoa_id=vinculo.id_pessoa,
                curso_id=vinculo.curso.id if vinculo.curso else None
            )
            for vinculo in pessoa.vinculos
        ]

        model = models.PessoaModel(
            id=pessoa.id,
            nome=pessoa.nome,
            cpf=pessoa.cpf,
            email=pessoa.email,
            data_nascimento=pessoa.data_nascimento,
            vinculos=vinculos_orm
        )

        try:
            with SessionLocal() as session:
                session.add(model)
                session.commit()
                session.refresh(model)  # Atualiza com ID e dados do BD
                return model
        except Exception as e:
            session.rollback()
            raise e
        
        return pessoa

    def buscar_por_cpf(self, cpf: int):
        try:
            with SessionLocal() as session:
                model = session.execute(
                    select(models.PessoaModel).where(models.PessoaModel.cpf == cpf)
                ).scalar_one_or_none()

            return model
        except Exception as e:
            raise e
    def buscar_por_email(self, email: str):
        try:
            with SessionLocal() as session:
                model = session.execute(
                    select(models.PessoaModel).where(models.PessoaModel.email == email)
                ).scalar_one_or_none()

            if model is None:
                return None

            return model
        except Exception as e:
            raise e
        
    def buscar_por_id(self, id: int):
        try:
            with SessionLocal() as session:
                model = session.get(models.PessoaModel, id)
                if model is None:
                    return None
                return model
        except Exception as e:
            raise e