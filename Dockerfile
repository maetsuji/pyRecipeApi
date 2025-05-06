## https://hub.docker.com/_/python

### Estágio 1: Ambiente de build ###
## Usa a imagem slim do Python como base
FROM python:3.13-slim AS builder
LABEL stage=builder
# FROM python:3.13.3-slim 
# FROM python:3

## Define o diretório de trabalho dentro do container
WORKDIR /pyrecipeapi

## Instala o venv e remove os arquivos de cache do apt
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

## Cria e ativa o ambiente virtual
RUN python3 -m venv /pyrecipeapi/venv
ENV PATH="/pyrecipeapi/venv/bin:$PATH"

## Instala as dependências do projeto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

## Verifica se o uvicorn foi instalado corretamente
RUN ls /pyrecipeapi/venv/bin && /pyrecipeapi/venv/bin/pip list
## Verifica se o ambiente virtual foi criado corretamente
RUN ls /pyrecipeapi/venv/bin && /pyrecipeapi/venv/bin/python --version

## Copia o código da aplicação para o container
COPY . /pyrecipeapi/

### Estágio 2: Ambiente de execução (distroless) ###
## Usa a versão slim do Python como base
# FROM gcr.io/distroless/python3-debian12:latest-amd64
FROM python:3.13-slim

## Define o diretório de trabalho dentro do container
WORKDIR /pyrecipeapi-runtime

## Copia o código da aplicação do estágio de build
COPY --from=builder /pyrecipeapi/ /pyrecipeapi-runtime/

## Define a variável de ambiente para usar o ambiente virtual
ENV PATH="/pyrecipeapi-runtime/venv/bin:$PATH"

## Expõe a porta em que o FastAPI será executado
EXPOSE 8000

## Define o diretório de trabalho para que `main.py` seja reconhecido como um módulo local
WORKDIR /pyrecipeapi-runtime/

## Executa o projeto
CMD ["/pyrecipeapi-runtime/venv/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
