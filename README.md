# suap_eleicao

## Usem a Branch: `develop`

### Subindo o ambiente

```bash
# Suba os containers com Docker Compose
docker compose up -d

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações do banco de dados
alembic upgrade head

# Gere os arquivos gRPC a partir do proto
python -m grpc_tools.protoc -I./protos --python_out=./gr --grpc_python_out=./gr ./protos/sysele.proto
Importante lembrar de entrar no sysele_pb2_grpc e mudar o import de: import sysele_pb2 as sysele__pb2 para: from gr import sysele_pb2 as sysele__pb2

# Rode o servidor
python gr/servidor.py --host 0.0.0.0 --port 8000
