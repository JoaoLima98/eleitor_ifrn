from models import models
from domain.curso import Curso
from infra.db import SessionLocal
from sqlalchemy import select, update

class CursoRepository:
    def salvar(self, curso: Curso):
        try:
            with SessionLocal() as session:
                # Verifica se já existe pelo id (update) ou cria novo
                if curso.id:
                    model = session.get(models.CursoModel, curso.id)
                    if not model:
                        model = models.CursoModel()
                else:
                    model = models.CursoModel()

                # Atualiza campos
                model.nome = curso.nome
                model.descricao = curso.descricao
                model.etapa_id = curso.etapa.id if curso.etapa else None

                session.add(model)
                session.commit()
                session.refresh(model)

                # Atualiza o id do domain para refletir o id do banco (se novo)
                curso.id = model.id

                return curso
        except Exception as e:
            raise e

    def buscar_por_id(self, curso_id: int):
        try:
            with SessionLocal() as session:
                model = session.get(models.CursoModel, curso_id)
                if model is None:
                    return None
                
                # Converte para domain Curso
                from domain.etapa import Etapa
                etapa_domain = Etapa(
                    id=model.etapa.id,
                    etapa=model.etapa.etapa,
                    turno=model.etapa.turno
                ) if model.etapa else None

                curso = Curso(
                    id=model.id,
                    nome=model.nome,
                    descricao=model.descricao,
                    etapa=etapa_domain
                )
                return curso
        except Exception as e:
            raise e
    def get_nome_by_nome(self, nome: str) -> bool:
        try:
            with SessionLocal() as session:
                result = session.execute(
                    select(models.CursoModel).where(models.CursoModel.nome == nome)
                ).scalar_one_or_none()
                return result is not None
        except Exception as e:
            raise e

    def atualizar(self, curso: Curso, curso_id: int):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    update(models.CursoModel)
                    .where(models.CursoModel.id == curso_id)
                    .values(nome=curso.nome, descricao=curso.descricao, etapa_id=curso.etapa.id)
                )
                session.commit()
                return result
        except Exception as e:
            raise e
        
    def remover(self, curso_id: int):
        try:
            with SessionLocal() as session:
                session.query(models.CursoModel).filter(models.CursoModel.id == curso_id).delete()
                session.commit()
        except Exception as e:
            raise e