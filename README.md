# Anotações de Elasticsearch para o TCC (PT-BR only)
Source: [Elasticsearch Labs](www.elastic.co/search-labs)

### // Execução do docker do Elastic **porta padrão: 9200**:
- `docker run -p 127.0.0.1:9200:9200 -d --name elasticsearch \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "xpack.license.self_generated.type=basic" \
  -v "elasticsearch-data:/usr/share/elasticsearch/data" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.0`

### // OBS: é possivel alterar o parâmetro "xpack.license.self_generated.type" para "trial" para um teste de 30 dias da licença oficial

## SEARCH TUTORIAL

### // Download dos arquivos base do projeto
- [Baixar](https://github.com/elastic/elasticsearch-labs/raw/main/example-apps/search-tutorial/search-tutorial-starter.zip)

### // Criação do ambiente virtual Python para execução do projeto
- `python -m venv .venv`

### // Execução do ambiente virtual Python **na pasta raiz** (requer permissões de administrador)
- [Linux/macOS] `source .venv/bin/activate`
- [Windows] `.venv\Scripts\activate`

### // OBS: para ter permissões de administrador no Windows, basta executar o comando:
- `Set-ExecutionPolicy RemoteSigned -Scope Process`

### // Para sair do ambiente virtual, basta executar o comando:
- `deactivate`

### // Instalação das dependências do projeto **na pasta 'search-tutorial'**:
- `pip install -r requirements.txt`

### // É necessário criar um arquivo .env com o conteúdo **na pasta 'search-tutorial'** com o conteúdo:
- `ELASTIC_URL="http://localhost:9200"`

### // Execução do Flask **porta padrão: 5001**:
- `flask run`

