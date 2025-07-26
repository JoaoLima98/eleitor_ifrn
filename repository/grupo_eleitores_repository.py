from sqlalchemy.orm import Session
from sqlalchemy import select
from models.grupo_eleitores_model import GrupoEleitoresModel
from models.eleitor_model import EleitorModel
from domain.grupo_eleitores import GrupoEleitores
from domain.eleitor import Eleitor
from gr.grupo_eleitores_pb2 import GrupoEleitoresMessage, EleitorMessage

class GrupoEleitoresRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, grupo: GrupoEleitores):
        model = GrupoEleitoresModel(
            id=grupo.id,
            nome=grupo.nome,
            descricao=grupo.descricao,
            ativo=grupo.ativo,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return grupo

    def buscar_por_nome(self, nome: str) -> GrupoEleitores | None:
        model = self.db.execute(
            select(GrupoEleitoresModel).where(GrupoEleitoresModel.nome == nome)
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
        model = self.db.get(GrupoEleitoresModel, grupo_id)
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
                vinculos=[]  # você pode carregar vínculos se quiser
            )
            grupo.append_lista_eleitores(eleitor)

        return grupo

    def nome_existe(self, nome: str) -> bool:
        return self.db.query(GrupoEleitoresModel).filter(GrupoEleitoresModel.nome == nome).first() is not None
    def adicionar_eleitor(self, grupo_id: int, eleitor: Eleitor):
        grupo = self.db.get(GrupoEleitoresModel, grupo_id)
        if not grupo:
            raise ValueError("Grupo de eleitores não encontrado.")

        eleitor_model = self.db.get(EleitorModel, eleitor.id)
        if not eleitor_model:
            raise ValueError("Eleitor não encontrado.")

        grupo.eleitores.append(eleitor_model)
        self.db.commit()
        self.db.refresh(grupo)
        return eleitor
    
    def remover_eleitor(self, grupo_id: int, eleitor: Eleitor):
        grupo = self.db.get(GrupoEleitoresModel, grupo_id)
        if not grupo:
            raise ValueError("Grupo de eleitores não encontrado.")

        eleitor_model = self.db.get(EleitorModel, eleitor.id)
        if not eleitor_model:
            raise ValueError("Eleitor não encontrado.")

        if eleitor_model not in grupo.eleitores:
            raise ValueError("Eleitor não está associado a este grupo.")

        grupo.eleitores.remove(eleitor_model)
        self.db.commit()
        self.db.refresh(grupo)
        return eleitor
    
    def listar_grupos(self) -> list[GrupoEleitores]:
        grupos = self.db.query(GrupoEleitoresModel).all()
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
                    vinculos=[]  # você pode carregar vínculos se quiser
                )
                grupo.append_lista_eleitores(eleitor)
            lista_grupos.append(grupo)
        return lista_grupos
        
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
