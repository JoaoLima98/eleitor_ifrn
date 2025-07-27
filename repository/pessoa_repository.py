from models import pessoa_model
from sqlalchemy import select
from sqlalchemy.orm import Session
from infra.db import get_session

class PessoaRepository:
    def __init__(self, db: Session = get_session()):
        self.db = db

    def salvar(self, pessoa):
        model = pessoa_model(
            id=pessoa.id,
            nome=pessoa.nome,
            cpf=pessoa.cpf,
            email=pessoa.email,
            data_nascimento=pessoa.data_nascimento
        )
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        except Exception as e:
            self.db.rollback()
            raise e
        return pessoa

    def buscar_por_cpf(self, cpf: int):
        try:
            model = self.db.execute(
                select(pessoa_model).where(pessoa_model.cpf == cpf)
            ).scalar_one_or_none()

            if model is None:
                return None

            return (
                model.id,
                model.nome,
                model.cpf,
                model.email,
                model.data_nascimento,
                model.vinculos
            )
        except Exception as e:
            raise e
    def buscar_por_email(self, email: str):
        try:
            model = self.db.execute(
                select(pessoa_model).where(pessoa_model.email == email)
            ).scalar_one_or_none()

            if model is None:
                return None

            return (
                model.id,
                model.nome,
                model.cpf,
                model.email,
                model.data_nascimento,
                model.vinculos
            )
        except Exception as e:
            raise e
        
    def buscar_por_id(self, id: int):
        try:
            model = self.db.get(pessoa_model, id)
            if model is None:
                return None

            return (
                model.id,
                model.nome,
                model.cpf,
                model.email,
                model.data_nascimento,
                model.vinculos
            )
        except Exception as e:
            raise e