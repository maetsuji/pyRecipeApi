### Estágio 1: Build com Python 3.13-slim ###
FROM python:3.13-slim AS builder
## Define o diretório de trabalho dentro do container
LABEL stage=builder
WORKDIR /api-build

## Atualiza e instala dependências necessárias apenas para o build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

## copia só o requirements para acelerar cache
COPY requirements.txt ./

## instala dependências em /app-dist
RUN pip install --no-cache-dir --target /api-build-depend -r requirements.txt

## copia o código da aplicação para o container
COPY ./app /api-build/app


### Estágio 2: Runtime com Distroless (ou seria se funcionasse :[ ) ###
# FROM gcr.io/distroless/python3-debian12:latest-amd64
FROM python:3.13-slim AS runtime
## Define o diretório de trabalho dentro do container
LABEL stage=runtime
WORKDIR /api-runtime

## traz código e dependências do builder
COPY --from=builder /api-build /api-runtime
COPY --from=builder /api-build-depend /api-runtime/api-runtime-depend
## define o diretório de trabalho para que `main.py` seja reconhecido como um módulo local

## adiciona dependências ao PYTHONPATH
ENV PYTHONPATH=/api-runtime/api-runtime-depend

## expõe porta do FastAPI
EXPOSE 8000

## executa uvicorn
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]