# pyRecipeAPI

Este é um projeto de API para gerenciar receitas e ingredientes, desenvolvido com **FastAPI** e **SQLAlchemy**.

## Sobre o Projeto

🇧🇷 - Este é um projeto de API Web em Python que gerencia Receitas e Ingredientes. Ele foi feito inicialmente em .NET e reescrito em Python como parte de um pré-projeto para o curso de DevOps da LACUNA Software e como um desafio pessoal para aprender mais sobre FastAPI, SQLAlchemy e requisições HTTP. Abaixo, você encontrará instruções sobre como configurar, executar e testar a API.

🇺🇸 - This is a Python Web API project that manages Recipes and Ingredients. It was initially built in .NET and rewritten in Python as part of a pre-project for the LACUNA Software DevOps course, and as a personal challenge to further explore FastAPI, SQLAlchemy, and HTTP requests. Below you will find instructions on how to set up, run, and test the API.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados no seu sistema:

- **`python 3.10` ou superior**
- **`pip`** (gerenciador de pacotes do Python): Ferramenta utilizada para instalar e gerenciar pacotes Python. Ele permite que você instale bibliotecas e dependências necessárias para o projeto diretamente do repositório PyPI.

- **`pip-tools`**: Conjunto de ferramentas que ajudam a gerenciar dependências Python de forma mais eficiente. Ele inclui o `pip-compile`, que gera um arquivo `requirements.txt` a partir de um arquivo `requirements.in`, e o `pip-sync`, que sincroniza o ambiente com as dependências especificadas.

- **`docker`**: Plataforma que permite criar, implantar e executar aplicativos em contêineres. Ele garante que o ambiente de execução seja consistente, independentemente do sistema operacional ou configuração da máquina.

- **`docker-compose`**: Ferramenta que facilita a definição e execução de aplicativos multi-contêiner. Com ele, é possível usar um arquivo `docker-compose.yaml` para configurar os serviços e gerenciá-los com comandos simples.
 
---

## Executando o projeto usando Docker:

### **Utilize o shell script providenciado com o projeto**:
1. **Clone o repositório**:
  ```bash
  git clone https://github.com/maetsuji/pyRecipeApi.git
  cd pyRecipe_API
  ```

2. **Rode o script a partir da raiz do projeto**:
  ```bash
  sudo sh pyrecipeapi.sh
  ```
  Esse script instala todas as dependências necessárias para executá-lo com sucesso.   
  Se utilizou esse script, parabéns! Os contêineres já estão no ar.

3. **Acesse a documentação interativa**:
  Abra o navegador e acesse: [**`http://127.0.0.1:8000/docs`**](http://127.0.0.1:8000/docs) (Swagger UI)

4. **Para interromper a execução:**
  ```bash
  docker stop pyrecipeapi-running
  ```
  ou simplesmente `[Ctrl + C]` no terminal em que o projeto está sendo executado.

---

### Configuração do Arquivo `.env`

Certifique-se de configurar o arquivo `.env` com as variáveis de ambiente corretas. Exemplo:

```env
DATABASE_URL=mysql+pymysql://root:root@db:3306/recipes
```

---

### Migração de Dados do SQLite para MySQL

No projeto, visando conteinerizar o banco de dados de forma separada da aplicação, precisei migrar de SQLite para MySQL.
Se você possui um banco de dados SQLite (`recipes.db`) com dados existentes, pode migrá-los para o MySQL utilizando o serviço `migrate`:

1. Certifique-se de que o arquivo `recipes.db` está no diretório raiz do projeto.
2. Execute o comando de migração:
  ```bash
  docker-compose run migrate
  ```
3. Verifique se os dados foram migrados corretamente acessando o banco de dados MySQL:
  ```bash
  docker exec -it <db_container_id> mysql -u root -p recipes
  ```

---

### Estrutura do Projeto

```plaintext
pyRecipe_API/
├── .env                  # Configurações de ambiente
├── requirements.txt      # Dependências do projeto
├── Dockerfile            # Especificações de como a aplicação será conteinerizada
├── docker-compose.yaml   # Configuração do Docker Compose
├── migrate_data.py       # Script de migração de dados
├── run_pyrecipeapi.sh    # Shell Script de configuração automática da API
└── app/
   ├── __init__.py       # Arquivo de inicialização do pacote
   ├── crud.py           # Operações CRUD para o banco de dados
   ├── database.py       # Configuração do banco de dados
   ├── main.py           # Ponto de entrada da aplicação
   ├── models.py         # Definições dos modelos do banco de dados
   ├── schemas.py        # Esquemas de validação e serialização
   └── __pycache__/      # Arquivos cacheados pelo Python
```

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
