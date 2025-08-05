from domain.pessoa import Pessoa
from domain.vinculo import Vinculo
from sqlalchemy import select, update
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
                id_pessoa=vinculo.id_pessoa,
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
    
    def atualizar(self, pessoa: Pessoa, id_pessoa: int):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    update(models.PessoaModel)
                    .where(models.PessoaModel.id == id_pessoa)
                    .values(nome=pessoa.nome,
                            cpf=pessoa.cpf,
                            email=pessoa.email,
                            data_nascimento=pessoa.data_nascimento,)
                )
                session.commit()
                return result
        except Exception as e:
            raise e
        
    def remover(self, id_pessoa: int):
        try:
            with SessionLocal() as session:
                session.query(models.PessoaModel).filter(models.PessoaModel.id == id_pessoa).delete()
                session.commit()
        except Exception as e:
            raise e
        
    def adicionar_vinculo(self, id_pessoa: int, vinculo: Vinculo):
        try:
            with SessionLocal() as session:
                pessoa = session.get(models.PessoaModel, id_pessoa)
                vinculo_novo = models.VinculoModel(
                id=vinculo.id,
                tipo=vinculo.tipo.value if hasattr(vinculo.tipo, "value") else vinculo.tipo,
                pessoa=pessoa,
                curso_id=vinculo.curso.id if vinculo.curso else None
            )
            session.add(vinculo_novo)
            session.commit()
            session.refresh(vinculo_novo)
        except Exception as e:
            raise e
