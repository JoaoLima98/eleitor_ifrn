from models.etapa_model import EtapaModel
from sqlalchemy.orm import Session
from domain.etapa import Etapa

class EtapaRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, etapa: Etapa):
        try:
            model = EtapaModel(
                etapa=etapa.etapa,
                turno=etapa.turno
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return etapa
        except Exception as e:
            self.db.rollback()
            raise e

    def get_etapa_and_turno_by_etapa_and_turno(self, etapa: int, turno: str) -> bool:
        return self.db.query(EtapaModel).filter(
            EtapaModel.etapa == etapa,
            EtapaModel.turno == turno
        ).first() is not None
        
    def buscar_por_id(self, etapa: int, turno: str) -> Etapa | None:
        try:
            model = self.db.query(EtapaModel).filter(
                EtapaModel.etapa == etapa,
                EtapaModel.turno == turno
            ).first()

            if model is None:
                return None

            return Etapa(
                etapa=model.etapa,
                turno=model.turno
            )
        except Exception as e:
            raise e
