from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models import models
from domain.grupo_eleitores import GrupoEleitores
from domain.enum.status import Status
from domain.eleitor import Eleitor
from gr.grupo_eleitores_pb2 import GrupoEleitoresMessage, EleitorMessage
from infra.db import SessionLocal

class GrupoEleitoresRepository:

    def salvar(self, grupo: GrupoEleitores):
        print(f"Salvando grupo no repositório: ID={grupo.id}, Nome={grupo.nome}")
        
        try:
            with SessionLocal() as session:
                # Verifica se já existe pelo id (update) ou cria novo
                if grupo.id and grupo.id > 0:  # Verifica se o ID é válido
                    print(f"Buscando grupo existente com ID: {grupo.id}")
                    model = session.get(models.GrupoEleitoresModel, grupo.id)
                    if not model:
                        print(f"Grupo com ID {grupo.id} não encontrado, criando novo")
                        model = models.GrupoEleitoresModel()
                else:
                    print("Criando novo grupo")
                    model = models.GrupoEleitoresModel()

                # Atualiza campos
                model.nome = grupo.nome
                model.descricao = grupo.descricao
                model.ativo = grupo.ativo

                session.add(model)
                session.commit()
                
                # IMPORTANTE: Atualiza o objeto original com o ID gerado pelo banco
                grupo.id = model.id
                
                print(f"Grupo salvo no banco: ID={model.id}, Nome={model.nome}")
                
                # Verifica se o grupo foi realmente salvo
                session.refresh(model)
                print(f"Grupo verificado no banco: ID={model.id}, Nome={model.nome}")
                
                return grupo  # Retorna o objeto atualizado
        except Exception as e:
            print(f"Erro ao salvar grupo no repositório: {str(e)}")
            raise e

    def buscar_por_id(self, grupo_id: int) -> GrupoEleitores | None:
        try:
            with SessionLocal() as db:
                # Carrega o grupo com todos os eleitores relacionados
                stmt = (
                    select(models.GrupoEleitoresModel)
                    .options(
                        # Carrega os eleitores usando o nome correto do relacionamento
                        selectinload(models.GrupoEleitoresModel.eleitores)
                    )
                    .where(models.GrupoEleitoresModel.id == grupo_id)
                )
                result = db.execute(stmt).scalar_one_or_none()
                
                if result is None:
                    return None
                    
                # Converte os eleitores do modelo para objetos de domínio
                lista_eleitores = []
                for eleitor_model in result.eleitores:
                    # Acessa os dados da pessoa através do relacionamento
                    pessoa = eleitor_model.pessoa
                    eleitor = Eleitor(
                        id=eleitor_model.id,
                        nome=pessoa.nome,
                        email=pessoa.email,
                        cpf=pessoa.cpf,
                        data_nascimento=pessoa.data_nascimento.strftime("%Y-%m-%d") if pessoa.data_nascimento else "",
                        status=Status(eleitor_model.status),
                        vinculos=[]
                    )
                    lista_eleitores.append(eleitor)
                
                # Cria o objeto de domínio com todos os dados
                grupo = GrupoEleitores(
                    id=result.id,
                    nome=result.nome,
                    descricao=result.descricao,
                    ativo=result.ativo,
                    lista_eleitores=lista_eleitores
                )
                
                return grupo
        except Exception as e:
            raise e

    def buscar_por_nome(self, grupo_nome: str) -> GrupoEleitores | None:
        try:
            with SessionLocal() as db:
                # Carrega o grupo com todos os eleitores relacionados
                stmt = (
                    select(models.GrupoEleitoresModel)
                    .options(selectinload(models.GrupoEleitoresModel.eleitores))  # Carrega os eleitores relacionados
                    .where(models.GrupoEleitoresModel.nome == grupo_nome)
                )
                result = db.execute(stmt).scalar_one_or_none()
                
                if result is None:
                    return None
                    
                # Converte os eleitores do modelo para objetos de domínio
                lista_eleitores = []
                for eleitor_model in result.eleitores:
                    eleitor = Eleitor(
                        id=eleitor_model.id,
                        nome=eleitor_model.pessoa.nome,  # Assumindo que EleitorModel tem relacionamento com PessoaModel
                        email=eleitor_model.pessoa.email,
                        cpf=eleitor_model.pessoa.cpf,
                        data_nascimento=eleitor_model.pessoa.data_nascimento,
                        status=Status(eleitor_model.status)
                    )
                    lista_eleitores.append(eleitor)
                
                # Cria o objeto de domínio com todos os dados
                grupo = GrupoEleitores(
                    id=result.id,
                    nome=result.nome,
                    descricao=result.descricao,
                    ativo=result.ativo,
                    lista_eleitores=lista_eleitores  # Adiciona a lista de eleitores convertidos
                )
                
                return grupo
        except Exception as e:
            raise e

    def adicionar_eleitor(self, grupo_id: int, eleitor_id):
        with SessionLocal() as session:
            grupo = session.get(models.GrupoEleitoresModel, grupo_id)
            if not grupo:
                raise ValueError("Grupo não encontrado.")

            # normaliza: aceita tanto o inteiro quanto o objeto de domínio que tem .id
            chave_eleitor = eleitor_id.id if hasattr(eleitor_id, "id") else eleitor_id

            eleitor = session.get(models.EleitorModel, chave_eleitor)
            if not eleitor:
                raise ValueError("Eleitor não encontrado.")

            if eleitor not in grupo.eleitores:
                grupo.eleitores.append(eleitor)

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
            stmt = select(models.GrupoEleitoresModel).options(
                selectinload(models.GrupoEleitoresModel.eleitores)
            )
            result = db.execute(stmt).scalars().all()

            lista_grupos = []

            for model in result:
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
                        vinculos=[]
                    )
                    grupo.append_lista_eleitores(eleitor)

                lista_grupos.append(grupo)

            return lista_grupos



    def atualizar(self, grupo: GrupoEleitores, grupo_id: int):
        try:
            with SessionLocal() as session:
                result = session.execute(
                    update(models.GrupoEleitoresModel)
                    .where(models.GrupoEleitoresModel.id == grupo_id)
                    .values(nome=grupo.nome,
                descricao=grupo.descricao,
                ativo=grupo.ativo)
                )
                session.commit()
                return result
        except Exception as e:
            raise e
        
    def remover(self, grupo_id: int):
        try:
            with SessionLocal() as session:
                session.query(models.GrupoEleitoresModel).filter(models.GrupoEleitoresModel.id == grupo_id).delete()
                session.commit()
        except Exception as e:
            raise e
    
    def listar_eleitores_por_grupo_id(self, grupo_id: int) -> list[Eleitor]:
        with SessionLocal() as db:
            stmt = (
                select(models.GrupoEleitoresModel)
                .options(selectinload(models.GrupoEleitoresModel.eleitores))
                .where(models.GrupoEleitoresModel.id == grupo_id)
            )
            result = db.execute(stmt).scalar_one_or_none()

            if result is None:
                return []

            eleitores = []

            for eleitor_model in result.eleitores:
                eleitor = Eleitor(
                    id=eleitor_model.id,
                    nome=eleitor_model.nome,
                    email=eleitor_model.email,
                    cpf=eleitor_model.cpf,
                    data_nascimento=eleitor_model.data_nascimento,
                    status=eleitor_model.status,
                    vinculos=[]  # ou carregue os vínculos aqui se necessário
                )
                eleitores.append(eleitor)

            return eleitores