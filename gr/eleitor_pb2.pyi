from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TipoVinculo(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIPO_DESCONHECIDO: _ClassVar[TipoVinculo]
    DISCENTE: _ClassVar[TipoVinculo]
    DOCENTE: _ClassVar[TipoVinculo]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATUS_DESCONHECIDO: _ClassVar[Status]
    ATIVO: _ClassVar[Status]
    INATIVO: _ClassVar[Status]
    SUSPENSO: _ClassVar[Status]
TIPO_DESCONHECIDO: TipoVinculo
DISCENTE: TipoVinculo
DOCENTE: TipoVinculo
STATUS_DESCONHECIDO: Status
ATIVO: Status
INATIVO: Status
SUSPENSO: Status

class Vinculo(_message.Message):
    __slots__ = ("id", "matricula", "tipo", "id_pessoa", "curso")
    ID_FIELD_NUMBER: _ClassVar[int]
    MATRICULA_FIELD_NUMBER: _ClassVar[int]
    TIPO_FIELD_NUMBER: _ClassVar[int]
    ID_PESSOA_FIELD_NUMBER: _ClassVar[int]
    CURSO_FIELD_NUMBER: _ClassVar[int]
    id: int
    matricula: str
    tipo: TipoVinculo
    id_pessoa: int
    curso: Curso
    def __init__(self, id: _Optional[int] = ..., matricula: _Optional[str] = ..., tipo: _Optional[_Union[TipoVinculo, str]] = ..., id_pessoa: _Optional[int] = ..., curso: _Optional[_Union[Curso, _Mapping]] = ...) -> None: ...

class Etapa(_message.Message):
    __slots__ = ("etapa", "turno")
    ETAPA_FIELD_NUMBER: _ClassVar[int]
    TURNO_FIELD_NUMBER: _ClassVar[int]
    etapa: int
    turno: str
    def __init__(self, etapa: _Optional[int] = ..., turno: _Optional[str] = ...) -> None: ...

class Curso(_message.Message):
    __slots__ = ("id", "nome", "descricao", "etapa")
    ID_FIELD_NUMBER: _ClassVar[int]
    NOME_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    ETAPA_FIELD_NUMBER: _ClassVar[int]
    id: int
    nome: str
    descricao: str
    etapa: Etapa
    def __init__(self, id: _Optional[int] = ..., nome: _Optional[str] = ..., descricao: _Optional[str] = ..., etapa: _Optional[_Union[Etapa, _Mapping]] = ...) -> None: ...

class Pessoa(_message.Message):
    __slots__ = ("id", "cpf", "email", "data_nascimento", "nome", "vinculos")
    ID_FIELD_NUMBER: _ClassVar[int]
    CPF_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    DATA_NASCIMENTO_FIELD_NUMBER: _ClassVar[int]
    NOME_FIELD_NUMBER: _ClassVar[int]
    VINCULOS_FIELD_NUMBER: _ClassVar[int]
    id: int
    cpf: str
    email: str
    data_nascimento: str
    nome: str
    vinculos: _containers.RepeatedCompositeFieldContainer[Vinculo]
    def __init__(self, id: _Optional[int] = ..., cpf: _Optional[str] = ..., email: _Optional[str] = ..., data_nascimento: _Optional[str] = ..., nome: _Optional[str] = ..., vinculos: _Optional[_Iterable[_Union[Vinculo, _Mapping]]] = ...) -> None: ...

class Eleitor(_message.Message):
    __slots__ = ("pessoa", "status")
    PESSOA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    pessoa: Pessoa
    status: Status
    def __init__(self, pessoa: _Optional[_Union[Pessoa, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ...) -> None: ...

class GrupoEleitores(_message.Message):
    __slots__ = ("id", "nome", "descricao", "ativo", "lista_eleitores")
    ID_FIELD_NUMBER: _ClassVar[int]
    NOME_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    ATIVO_FIELD_NUMBER: _ClassVar[int]
    LISTA_ELEITORES_FIELD_NUMBER: _ClassVar[int]
    id: int
    nome: str
    descricao: str
    ativo: bool
    lista_eleitores: _containers.RepeatedCompositeFieldContainer[Eleitor]
    def __init__(self, id: _Optional[int] = ..., nome: _Optional[str] = ..., descricao: _Optional[str] = ..., ativo: bool = ..., lista_eleitores: _Optional[_Iterable[_Union[Eleitor, _Mapping]]] = ...) -> None: ...

class EnviarGrupoResponse(_message.Message):
    __slots__ = ("mensagem",)
    MENSAGEM_FIELD_NUMBER: _ClassVar[int]
    mensagem: str
    def __init__(self, mensagem: _Optional[str] = ...) -> None: ...
