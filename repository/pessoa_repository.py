from infra.models.pessoa_model import PessoaModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.pessoa import Pessoa

class PessoaRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pessoa: Pessoa):
        model = PessoaModel(
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

    def buscar_por_id(self, pessoa_id: int) -> Pessoa | None:
        try:
            model = self.db.execute(
                select(PessoaModel).where(PessoaModel.id == pessoa_id)
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
