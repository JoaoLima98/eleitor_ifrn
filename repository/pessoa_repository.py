from models import pessoa_model
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.pessoa import Pessoa

class PessoaRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pessoa: Pessoa):
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

    def buscar_por_cpf(self, cpf: int) -> Pessoa | None:
        try:
            model = self.db.execute(
                select(pessoa_model).where(pessoa_model.cpf == cpf)
            ).scalar_one_or_none()

            if model is None:
                return None

            return Pessoa(
                id=model.id,
                nome=model.nome,
                cpf=model.cpf,
                email=model.email,
                data_nascimento=model.data_nascimento,
                vinculos=[]  # pode ser carregado separadamente
            )
        except Exception as e:
            raise e
    def buscar_por_email(self, email: str) -> Pessoa | None:
        try:
            model = self.db.execute(
                select(pessoa_model).where(pessoa_model.email == email)
            ).scalar_one_or_none()

            if model is None:
                return None

            return Pessoa(
                id=model.id,
                nome=model.nome,
                cpf=model.cpf,
                email=model.email,
                data_nascimento=model.data_nascimento,
                vinculos=[]  # pode ser carregado separadamente
            )
        except Exception as e:
            raise e
        
    def buscar_por_id(self, id: int) -> Pessoa | None:
        try:
            model = self.db.get(pessoa_model, id)
            if model is None:
                return None

            return Pessoa(
                id=model.id,
                nome=model.nome,
                cpf=model.cpf,
                email=model.email,
                data_nascimento=model.data_nascimento,
                vinculos=[]  # pode ser carregado separadamente
            )
        except Exception as e:
            raise e