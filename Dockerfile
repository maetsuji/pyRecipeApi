# https://hub.docker.com/_/python

FROM python:3.10-slim
#FROM python:3

# Define o working directory dentro do container
WORKDIR /app

# Instala as dependências do sistema
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto para o container
COPY . ./

# Expõe a porta em que o FastAPI será executado
EXPOSE 8000

# Roda o projeto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# exemplo de dockerfile para .net
# FROM image_dotnet
# RUN install ___ (mysql)
# COPY . ./
# RUN build
# ENTRYPOINT ["dotnet", "minha.dll"]
# docker build -t my-python-app .
# docker run -it --rm --name my-running-app my-python-app
