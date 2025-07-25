from infra.models.vinculo_model import VinculoModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from domain.vinculo import Vinculo

class VinculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, vinculo: Vinculo):
        model = VinculoModel(
            id=vinculo.id,
            tipo=vinculo.tipo,
            pessoa_id=vinculo.pessoa_id
        )
        try:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return vinculo
        except Exception as e:
            self.db.rollback()
            raise e

    def buscar_por_id(self, vinculo_id: int) -> Vinculo | None:
        try:
            model = self.db.execute(
                select(VinculoModel).where(VinculoModel.id == vinculo_id)
            ).scalar_one_or_none()

            if model is None:
                return None

            return Vinculo(
                id=model.id,
                tipo=model.tipo,
                pessoa_id=model.pessoa_id
            )
        except Exception as e:
            raise e
