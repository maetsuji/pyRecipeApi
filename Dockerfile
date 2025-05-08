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

## copia estritamente o código da aplicação para o container
COPY ./app /api-build/app

## tentativa GPTosa de corrigir para a versao distroless ##
## Copy compiled dependencies (e.g., pydantic_core) and shared libraries
# RUN mkdir /api-build/libs && \
#    cp -r /api-build-depend/pydantic_core /api-build/libs/ && \
#    ldd $(find /api-build-depend -name "*.so") | awk '{print $3}' | grep -v '^(' | xargs -I '{}' cp -v '{}' /api-build/libs/

### Estágio 2: Runtime com Distroless (ou seria se funcionasse :[ ) ###
# FROM gcr.io/distroless/python3-debian12 AS runtime
FROM python:3.13-slim AS runtime
LABEL stage=runtime
WORKDIR /api-runtime

## Copia código e dependências do estágio de build
COPY --from=builder /api-build /api-runtime
COPY --from=builder /api-build-depend /api-runtime/api-runtime-depend
# COPY --from=builder /api-build/libs /lib     
## ^^^ parte da solucao gptosa

## Define o PYTHONPATH para incluir dependências
ENV PYTHONPATH=/api-runtime/api-runtime-depend
# ENV LD_LIBRARY_PATH=/lib:$LD_LIBRARY_PATH         
## ^^^ parte da solucao gptosa

## Expõe a porta do FastAPI
EXPOSE 8000

## Define o comando de execução
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]

## debuggando, aparentemente o comando de execução distroless. por que? pois existe apenas o runtime do python?
# CMD ["-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]