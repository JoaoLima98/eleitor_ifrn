from models import models
from domain.etapa import Etapa
from infra.db import SessionLocal
from sqlalchemy import select

class EtapaRepository:
    def salvar(self, etapa):
        try:
            with SessionLocal() as session:
                existente = session.execute(
                    select(models.EtapaModel).where(
                        models.EtapaModel.etapa == etapa.etapa,
                        models.EtapaModel.turno == etapa.turno
                    )
                ).scalar_one_or_none()

                if existente:
                    return existente

                model = models.EtapaModel(
                    etapa=etapa.etapa,
                    turno=etapa.turno
                )
                session.add(model)
                session.commit()
                session.refresh(model)
                return model
        except Exception as e:
            session.rollback()
            raise ValueError("Etapa duplicada no banco.")
        except Exception as e:
            raise e

    def get_etapa_and_turno_by_etapa_and_turno(self, etapa: int, turno: str) -> bool:
        try:
            with SessionLocal() as session:
                result = session.execute(
                    select(models.EtapaModel).where(
                        models.EtapaModel.etapa == etapa,
                        models.EtapaModel.turno == turno
                    )
                ).first()
                return result is not None
        except Exception as e:
            raise e

    def buscar_por_id(self, id: int):
        try:
            with SessionLocal() as session:
                model = session.get(models.EtapaModel, id)
                if model is None:
                    return None
                return (model.id, model.etapa, model.turno)
        except Exception as e:
            raise e
