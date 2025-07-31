from sqlalchemy import select
from models import models
from domain.grupo_eleitores import GrupoEleitores
from domain.eleitor import Eleitor
from gr.grupo_eleitores_pb2 import GrupoEleitoresMessage, EleitorMessage
from infra.db import SessionLocal

class GrupoEleitoresRepository:

    def salvar(self, grupo: GrupoEleitores):
        with SessionLocal() as db:
            model = models.GrupoEleitoresModel(
                nome=grupo.nome,
                descricao=grupo.descricao,
                ativo=grupo.ativo,
            )
            db.add(model)
            db.commit()
            db.refresh(model)
            return grupo

    def buscar_por_nome(self, nome: str) -> GrupoEleitores | None:
        with SessionLocal() as db:
            model = db.execute(
                select(models.GrupoEleitoresModel).where(models.GrupoEleitoresModel.nome == nome)
            ).scalar_one_or_none()

            if model is None:
                return None

            return GrupoEleitores(
                id=model.id,
                nome=model.nome,
                descricao=model.descricao,
                ativo=model.ativo
            )

    def buscar_por_id(self, grupo_id: int) -> GrupoEleitores | None:
        with SessionLocal() as db:
            model = db.get(models.GrupoEleitoresModel, grupo_id)
            if model is None:
                return None

            grupo = GrupoEleitores(
                id=model.id,
                nome=model.nome,
                descricao=model.descricao,
                ativo=model.ativo
            )

            for eleitor_model in model.eleitores:
                eleitor = Eleitor(
                    id=eleitor_model.id,
                    nome=eleitor_model.nome,
                    email=eleitor_model.email,
                    cpf=eleitor_model.cpf,
                    data_nascimento=eleitor_model.data_nascimento,
                    status=eleitor_model.status,
                    vinculos=[]  # pode carregar vínculos se quiser
                )
                grupo.append_lista_eleitores(eleitor)

            return grupo

    def nome_existe(self, nome: str) -> bool:
        with SessionLocal() as db:
            return db.query(models.GrupoEleitoresModel).filter(models.GrupoEleitoresModel.nome == nome).first() is not None

    def adicionar_eleitor(self, grupo_id: int, eleitor_id):
        with SessionLocal() as session:
            grupo = session.get(models.GrupoEleitoresModel, grupo_id)
            if not grupo:
                raise ValueError("Grupo não encontrado.")

            eleitor = session.get(models.EleitorModel, eleitor_id)
            if not eleitor:
                raise ValueError("Eleitor não encontrado.")

            if eleitor not in grupo.eleitores:
                grupo.eleitores.append(eleitor)  # Só isso já adiciona na tabela intermediária!
            
            session.commit()
            session.refresh(grupo)
            return grupo



    def remover_eleitor(self, grupo_id: int, eleitor: Eleitor):
        with SessionLocal() as db:
            grupo = db.get(models.GrupoEleitoresModel, grupo_id)
            if not grupo:
                raise ValueError("Grupo de eleitores não encontrado.")

            eleitor_model = db.get(models.EleitorModel, eleitor.id)  # corrigido para EleitorModel
            if not eleitor_model:
                raise ValueError("Eleitor não encontrado.")

            if eleitor_model not in grupo.eleitores:
                raise ValueError("Eleitor não está associado a este grupo.")

            grupo.eleitores.remove(eleitor_model)
            db.commit()
            db.refresh(grupo)
            return eleitor

    def listar_grupos(self) -> list[GrupoEleitores]:
        with SessionLocal() as db:
            grupos = db.query(models.GrupoEleitoresModel).all()
            lista_grupos = []
            for model in grupos:
                grupo = GrupoEleitores(
                    id=model.id,
                    nome=model.nome,
                    descricao=model.descricao,
                    ativo=model.ativo
                )
                for eleitor_model in model.eleitores:
                    eleitor = Eleitor(
                        id=eleitor_model.id,
                        nome=eleitor_model.nome,
                        email=eleitor_model.email,
                        cpf=eleitor_model.cpf,
                        data_nascimento=eleitor_model.data_nascimento,
                        status=eleitor_model.status,
                        vinculos=[]  # pode carregar vínculos se quiser
                    )
                    grupo.append_lista_eleitores(eleitor)
                lista_grupos.append(grupo)
            return lista_grupos

    @staticmethod
    def grupo_to_grpc(grupo: GrupoEleitores):
        return GrupoEleitoresMessage(
            id=grupo.id,
            nome=grupo.nome,
            descricao=grupo.descricao,
            ativo=grupo.ativo,
            data_cadastro=grupo.data_cadastro.isoformat(),
            data_atualizacao=grupo.data_atualizacao.isoformat(),
            lista_eleitores=[
                EleitorMessage(
                    id=e.id,
                    nome=e.nome,
                    email=e.email,
                    cpf=e.cpf,
                    data_nascimento=e.data_nascimento.isoformat(),
                    status=e.status.name
                ) for e in grupo.lista_eleitores
            ]
        )
