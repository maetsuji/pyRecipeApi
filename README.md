
# pyRecipeAPI

Este é um projeto de API para gerenciar receitas e ingredientes, desenvolvido com **FastAPI** e **SQLAlchemy**.

## Sobre o Projeto

🇧🇷 - Este é um projeto de API Web em Python que gerencia Receitas e Ingredientes. Ele foi feito inicialmente em .NET e reescrito em Python como parte de um pré-projeto para o curso de DevOps da LACUNA Software e como um desafio pessoal para aprender mais sobre FastAPI, SQLAlchemy e requisições HTTP. Abaixo, você encontrará instruções sobre como configurar, executar e testar a API.

🇺🇸 - This is a Python Web API project that manages Recipes and Ingredients. It was initially built in .NET and rewritten in Python as part of a pre-project for the LACUNA Software DevOps course, and as a personal challenge to further explore FastAPI, SQLAlchemy, and HTTP requests. Below you will find instructions on how to set up, run, and test the API.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados no seu sistema:

- Python 3.10 ou superior
- `pip` (gerenciador de pacotes do Python)
- `virtualenv` (opcional, mas recomendado)

---

## Configuração do Ambiente

### 1. Usando Docker:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/maetsuji/pyRecipeApi.git
   cd pyRecipe_API
   ```

2. **Construa utilizando `docker build`:**
   ```bash
   docker build -t pyrecipeapi .
   ```
   Esse comando cria uma imagem Docker chamada `pyrecipeapi` usando o arquivo `Dockerfile` localizado no diretório atual.

3. **Rode utilizando `docker run`:**
   ```bash
   docker run -d -p 8000:8000 --env-file .env -it --rm --name pyrecipeapi-running pyrecipeapi
   ```
   Esse comando executa o contêiner Docker da imagem pyrecipeapi:
   - **`-d`**: Executa o contêiner em modo detached (em segundo plano), permitindo que ele continue rodando sem bloquear o terminal.
   - **`-p 8000:8000`**: Mapeia a porta 8000 do contêiner para o host.
   - **`--env-file .env`**: Carrega variáveis de ambiente do arquivo `.env`.
   - **`-it`**: Permite interação com o terminal.
   - **`--rm`**: Remove o contêiner ao parar.
   - **`--name`**: Nomeia o contêiner como `pyrecipeapi-running`.


4. **Acesse a documentação interativa**:
   - Abra o navegador e acesse: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)


5. **Para interromper a execução:**
   ```bash
   docker stop pyrecipeapi-running
   ```

### 2. Configurando o ambiente manualmente:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/maetsuji/pyRecipeApi.git
   cd pyRecipe_API
   ```

2. **Crie e ative um ambiente virtual** (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o arquivo `.env`**:
   Configure as variáveis de ambiente necessárias no arquivo `.env`. Padrão:
   ```
   DATABASE_URL=sqlite:///./recipes.db
   ```

5. **Inicializando o banco de dados**:
   O banco de dados será automaticamente criado e configurado ao iniciar o projeto.

### Executando o Projeto

1. **Inicie o servidor FastAPI**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Acesse a documentação interativa**:
   - Abra o navegador e acesse: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
   - Ou acesse: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (Redoc)

---

## Endpoints da API

### **1. Ingredients**

#### **GET /api/ingredients**
Retorna todos os ingredientes cadastrados.

Exemplo de requisição:
```bash
curl -X GET "http://127.0.0.1:8000/api/ingredients"
```

---

#### **POST /api/ingredients**
Cria um ingrediente individual.

Exemplo de requisição:
```bash
curl -X POST "http://127.0.0.1:8000/api/ingredients" \
-H "Content-Type: application/json" \
-d '{
  "name": "Tomato",
  "unit_of_measure": "units"
}'
```

---

#### **POST /api/ingredients/bulk**
Cria múltiplos ingredientes em uma única requisição.

Exemplo de requisição:
```bash
curl -X POST "http://127.0.0.1:8000/api/ingredients/bulk" \
-H "Content-Type: application/json" \
-d '{
  "ingredients": [
    { "name": "Salt", "unit_of_measure": "teaspoons" },
    { "name": "Olive Oil", "unit_of_measure": "mililiters" }
  ]
}'
```

---

#### **PUT /api/ingredients/{id}**
Atualiza um ingrediente existente.

Exemplo de requisição:
```bash
curl -X PUT "http://127.0.0.1:8000/api/ingredients/1" \
-H "Content-Type: application/json" \
-d '{
  "name": "Tomato",
  "unit_of_measure": "kilograms"
}'
```

---

#### **DELETE /api/ingredients/{id}**
Deleta um ingrediente pelo ID.

Exemplo de requisição:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/ingredients/1"
```

---

### **2. Recipes**

#### **GET /api/recipes**
Retorna todas as receitas cadastradas.

Exemplo de requisição:
```bash
curl -X GET "http://127.0.0.1:8000/api/recipes"
```

---

#### **POST /api/recipes**
Cria uma receita individual.

Exemplo de requisição:
```bash
curl -X POST "http://127.0.0.1:8000/api/recipes" \
-H "Content-Type: application/json" \
-d '{
  "name": "Tomato Salad",
  "preparation_method": "Chop tomatoes and lettuce, drizzle olive oil, add salt and pepper, then toss gently.",
  "ingredients": [
    { "ingredient_id": 1, "quantity": 2 },
    { "ingredient_id": 2, "quantity": 0.5 }
  ]
}'
```

---

#### **POST /api/recipes/bulk**
Cria múltiplas receitas em uma única requisição.

Exemplo de requisição:
```bash
curl -X POST "http://127.0.0.1:8000/api/recipes/bulk" \
-H "Content-Type: application/json" \
-d '{
  "recipes": [
    {
      "name": "Salted Tomatoes",
      "preparation_method": "Slice the tomatoes, sprinkle salt, and let them rest for a few minutes before serving.",
      "ingredients": [
        { "ingredient_id": 1, "quantity": 3 },
        { "ingredient_id": 2, "quantity": 2 }
      ]
    },
    {
      "name": "Basic Omelette",
      "preparation_method": "Whisk eggs with salt and pepper, melt butter in a pan, pour the mixture, let it set, then fold.",
      "ingredients": [
        { "ingredient_id": 2, "quantity": 0.5 },
        { "ingredient_id": 4, "quantity": 0.25 }
      ]
    }
  ]
}'
```

---

#### **PUT /api/recipes/{id}**
Atualiza uma receita existente.

Exemplo de requisição:
```bash
curl -X PUT "http://127.0.0.1:8000/api/recipes/1" \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated Recipe Name",
  "preparation_method": "Updated preparation method.",
  "ingredients": [
    { "ingredient_id": 1, "quantity": 5 }
  ]
}'
```

---

#### **DELETE /api/recipes/{id}**
Deleta uma receita pelo ID.

Exemplo de requisição:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/recipes/1"
```

---

## Estrutura do Projeto

```
pyRecipe_API/
├── .env                  # Configurações de ambiente
├── recipes.db            # Banco de dados SQLite
├── requirements.in       # Dependências do projeto (arquivo de entrada)
├── requirements.txt      # Dependências do projeto (arquivo gerado)
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
