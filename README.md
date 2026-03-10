# 📋 API de Gerenciamento de Tarefas

API RESTful desenvolvida com **Flask + SQLAlchemy** para gerenciamento de tarefas e usuários, seguindo o padrão de arquitetura em camadas com **Models**, **DTOs**, **Mappers**, **Repositories** e **Routes**.

---

## 📑 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Arquitetura em Camadas](#-arquitetura-em-camadas)
  - [Models (Modelos)](#1-models-modelos)
  - [DTOs (Data Transfer Objects)](#2-dtos-data-transfer-objects)
  - [Mappers (Mapeadores)](#3-mappers-mapeadores)
  - [Repositories (Repositórios)](#4-repositories-repositórios)
  - [Routes (Rotas)](#5-routes-rotas)
- [Endpoints da API](#-endpoints-da-api)
  - [Usuários](#usuários)
  - [Tarefas](#tarefas)
- [Documentação Swagger](#-documentação-swagger)
- [Interface Web (Front-end)](#-interface-web-front-end)
- [Banco de Dados](#-banco-de-dados)

---

## 🔍 Visão Geral

Este sistema permite:

- **Cadastrar usuários** com nome e e-mail
- **Criar tarefas** vinculadas a um usuário
- **Listar, editar e excluir tarefas**
- **Marcar tarefas como concluídas**

O relacionamento entre as entidades é **1:N** — um usuário pode ter várias tarefas, mas cada tarefa pertence a um único usuário.

```
User 1 ──────── N Task
```

---

## 🛠 Tecnologias

| Tecnologia | Versão | Descrição |
|---|---|---|
| Python | 3.x | Linguagem principal |
| Flask | 3.1.0 | Framework web |
| Flask-SQLAlchemy | 3.1.1 | ORM para banco de dados |
| flask-swagger-ui | 4.11.1 | Interface Swagger UI |
| SQLite | — | Banco de dados (arquivo local) |
| Bootstrap | 5.3 | Framework CSS do front-end |

---

## 📂 Estrutura do Projeto

```
API_V2/
│
├── app.py                    # Ponto de entrada da aplicação
├── config.py                 # Configurações (banco de dados, etc.)
├── requirements.txt          # Dependências do projeto
│
├── models/                   # Camada de Modelos (ORM)
│   ├── __init__.py           # Instância do SQLAlchemy (db)
│   ├── user.py               # Modelo User
│   └── task.py               # Modelo Task
│
├── dtos/                     # Camada de Data Transfer Objects
│   ├── __init__.py
│   ├── user_dto.py           # DTO do Usuário
│   └── task_dto.py           # DTO da Tarefa
│
├── mappers/                  # Camada de Mapeadores
│   ├── __init__.py
│   ├── user_mapper.py        # Mapper User ↔ UserDTO
│   └── task_mapper.py        # Mapper Task ↔ TaskDTO
│
├── repositories/             # Camada de Repositórios (acesso a dados)
│   ├── __init__.py
│   ├── user_repository.py    # Repositório de Usuários
│   └── task_repository.py    # Repositório de Tarefas
│
├── routes/                   # Camada de Rotas (controllers)
│   ├── __init__.py
│   ├── user_routes.py        # Endpoints de Usuários
│   └── task_routes.py        # Endpoints de Tarefas
│
├── templates/                # Templates HTML (front-end)
│   └── index.html            # Interface web principal
│
└── docs/                     # Documentação da API
    └── swagger.yaml          # Especificação OpenAPI 3.0
```

---

## 🚀 Instalação e Execução

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação

```bash
python app.py
```

### 3. Acessar

| URL | Descrição |
|---|---|
| `http://localhost:5000` | Interface web (front-end) |
| `http://localhost:5000/docs` | Documentação Swagger UI |

O banco de dados SQLite (`tasks.db`) é criado automaticamente na primeira execução.

---

## 🏗 Arquitetura em Camadas

O projeto segue uma arquitetura em camadas que separa responsabilidades, facilitando manutenção e testes. O fluxo de uma requisição segue o caminho:

```
Requisição HTTP → Route → Mapper → Repository → Model/DB
                    ↓
               Resposta ← DTO ← Mapper ← Repository ← Model/DB
```

### 1. Models (Modelos)

**Pasta:** `models/`

Os **Models** representam as tabelas do banco de dados usando o ORM SQLAlchemy. Cada model é uma classe Python que mapeia diretamente para uma tabela.

#### User (`models/user.py`)

Representa a tabela `users` no banco.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | Integer | PK, auto-incremento | Identificador único |
| `name` | String(100) | NOT NULL | Nome do usuário |
| `email` | String(100) | NOT NULL, UNIQUE | E-mail do usuário |

- Possui um **relacionamento 1:N** com `Task` através de `db.relationship("Task")`
- O parâmetro `cascade="all, delete-orphan"` garante que ao excluir um usuário, todas as suas tarefas são excluídas automaticamente
- O `backref="user"` permite acessar o usuário de uma tarefa via `task.user`

```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan")
```

#### Task (`models/task.py`)

Representa a tabela `tasks` no banco.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | Integer | PK, auto-incremento | Identificador único |
| `title` | String(100) | NOT NULL | Título da tarefa |
| `description` | String(200) | — | Descrição da tarefa |
| `completed` | Boolean | Default: `False` | Status de conclusão |
| `user_id` | Integer | FK → `users.id`, NOT NULL | Usuário dono da tarefa |

- A coluna `user_id` é uma **chave estrangeira (Foreign Key)** que referencia `users.id`
- O campo `completed` inicia como `False` por padrão

```python
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
```

---

### 2. DTOs (Data Transfer Objects)

**Pasta:** `dtos/`

Os **DTOs** são objetos simples usados para **transportar dados** entre as camadas da aplicação. Eles definem **exatamente quais campos** serão expostos na resposta da API, evitando expor detalhes internos do modelo (como relacionamentos ou campos sensíveis).

#### Por que usar DTOs?

- **Desacoplamento:** A estrutura da resposta da API não depende diretamente da estrutura do banco de dados
- **Segurança:** Permite controlar quais campos são expostos (ex.: não expor `user_id` na resposta da tarefa)
- **Serialização:** O método `to_dict()` converte o DTO em dicionário, facilitando a conversão para JSON

#### UserDTO (`dtos/user_dto.py`)

```python
class UserDTO:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
```

**Exemplo de saída JSON:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com"
}
```

#### TaskDTO (`dtos/task_dto.py`)

```python
class TaskDTO:
    def __init__(self, id, title, description, completed):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
        }
```

**Exemplo de saída JSON:**
```json
{
  "id": 1,
  "title": "Estudar Python",
  "description": "Revisar DTO e Repository",
  "completed": false
}
```

---

### 3. Mappers (Mapeadores)

**Pasta:** `mappers/`

Os **Mappers** são responsáveis por **converter dados entre camadas**. Eles fazem a ponte entre os Models (entidades do banco) e os DTOs (objetos de transferência).

Cada Mapper possui dois métodos estáticos:

| Método | Direção | Descrição |
|---|---|---|
| `to_dto(entity)` | Model → DTO | Converte uma entidade do banco para um DTO (para respostas da API) |
| `to_entity(data)` | Dict → Model | Converte dados recebidos (JSON) em uma entidade do banco (para persistência) |

#### UserMapper (`mappers/user_mapper.py`)

```python
class UserMapper:

    @staticmethod
    def to_dto(user):
        return UserDTO(user.id, user.name, user.email)

    @staticmethod
    def to_entity(data):
        return User(name=data["name"], email=data["email"])
```

**Fluxo:**
- **Criação (POST):** JSON `{"name": "João", "email": "joao@email.com"}` → `to_entity()` → objeto `User`
- **Leitura (GET):** objeto `User` → `to_dto()` → `UserDTO` → `.to_dict()` → JSON

#### TaskMapper (`mappers/task_mapper.py`)

```python
class TaskMapper:

    @staticmethod
    def to_dto(task):
        return TaskDTO(task.id, task.title, task.description, task.completed)

    @staticmethod
    def to_entity(data):
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            completed=False,
            user_id=data["user_id"],
        )
```

- No `to_entity()`, o campo `completed` é sempre definido como `False` (tarefa nova nunca começa concluída)
- O `user_id` é obrigatório na criação para vincular a tarefa ao usuário

---

### 4. Repositories (Repositórios)

**Pasta:** `repositories/`

Os **Repositories** encapsulam toda a **lógica de acesso ao banco de dados**. Nenhuma outra camada interage diretamente com o SQLAlchemy — todas as operações passam pelo repositório.

#### Métodos disponíveis

| Método | Descrição |
|---|---|
| `get_all()` | Retorna todos os registros da tabela |
| `get_by_id(id)` | Busca um registro pelo ID (retorna `None` se não encontrado) |
| `save(entity)` | Insere ou atualiza um registro no banco |
| `delete(entity)` | Remove um registro do banco |

#### UserRepository (`repositories/user_repository.py`)

```python
class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, id):
        return db.session.get(User, id)

    def save(self, user):
        db.session.add(user)
        db.session.commit()

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
```

#### TaskRepository (`repositories/task_repository.py`)

```python
class TaskRepository:

    def get_all(self):
        return Task.query.all()

    def get_by_id(self, id):
        return db.session.get(Task, id)

    def save(self, task):
        db.session.add(task)
        db.session.commit()

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()
```

#### Por que usar Repositories?

- **Centralização:** Toda lógica de persistência fica em um só lugar
- **Desacoplamento:** As rotas não precisam conhecer detalhes do SQLAlchemy
- **Testabilidade:** Facilita a criação de mocks para testes unitários
- **Manutenção:** Se o banco de dados mudar, só o repositório precisa ser alterado

---

### 5. Routes (Rotas)

**Pasta:** `routes/`

As **Routes** definem os **endpoints da API** e orquestram o fluxo entre as camadas. Cada rota:

1. Recebe a requisição HTTP
2. Valida os dados de entrada
3. Usa o **Mapper** para converter dados
4. Usa o **Repository** para acessar o banco
5. Retorna a resposta em JSON usando o **DTO**

As rotas são organizadas em **Blueprints** do Flask, permitindo modularização.

#### User Routes (`routes/user_routes.py`)

```python
user_bp = Blueprint("users", __name__)
user_repo = UserRepository()
```

#### Task Routes (`routes/task_routes.py`)

```python
task_bp = Blueprint("tasks", __name__)
task_repo = TaskRepository()
user_repo = UserRepository()
```

O `task_routes` também instancia um `UserRepository` para validar se o usuário existe antes de criar uma tarefa.

---

## 📡 Endpoints da API

### Usuários

#### `GET /users` — Listar todos os usuários

**Resposta `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "João Silva",
    "email": "joao@email.com"
  }
]
```

---

#### `POST /users` — Criar um novo usuário

**Body (JSON):**
```json
{
  "name": "João Silva",
  "email": "joao@email.com"
}
```

**Resposta `201 Created`:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com"
}
```

**Resposta `400 Bad Request`** (campos faltando):
```json
{
  "error": "Campos 'name' e 'email' são obrigatórios"
}
```

---

#### `GET /users/{id}` — Buscar usuário por ID

**Resposta `200 OK`:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com"
}
```

**Resposta `404 Not Found`:**
```json
{
  "error": "Usuário não encontrado"
}
```

---

### Tarefas

#### `GET /tasks` — Listar todas as tarefas

**Resposta `200 OK`:**
```json
[
  {
    "id": 1,
    "title": "Estudar Python",
    "description": "Revisar DTO e Repository",
    "completed": false
  }
]
```

---

#### `POST /tasks` — Criar uma nova tarefa

**Body (JSON):**
```json
{
  "title": "Estudar Python",
  "description": "Revisar DTO e Repository",
  "user_id": 1
}
```

**Resposta `201 Created`:**
```json
{
  "id": 1,
  "title": "Estudar Python",
  "description": "Revisar DTO e Repository",
  "completed": false
}
```

**Resposta `400 Bad Request`:**
```json
{
  "error": "Campos 'title' e 'user_id' são obrigatórios"
}
```

**Resposta `404 Not Found`** (usuário inexistente):
```json
{
  "error": "Usuário não encontrado"
}
```

---

#### `GET /tasks/{id}` — Buscar tarefa por ID

**Resposta `200 OK`:**
```json
{
  "id": 1,
  "title": "Estudar Python",
  "description": "Revisar DTO e Repository",
  "completed": false
}
```

**Resposta `404 Not Found`:**
```json
{
  "error": "Tarefa não encontrada"
}
```

---

#### `PUT /tasks/{id}` — Atualizar uma tarefa

**Body (JSON):** (todos os campos são opcionais)
```json
{
  "title": "Estudar Flask",
  "description": "Focar em rotas e blueprints",
  "completed": true
}
```

**Resposta `200 OK`:**
```json
{
  "id": 1,
  "title": "Estudar Flask",
  "description": "Focar em rotas e blueprints",
  "completed": true
}
```

**Resposta `404 Not Found`:**
```json
{
  "error": "Tarefa não encontrada"
}
```

---

#### `DELETE /tasks/{id}` — Deletar uma tarefa

**Resposta `204 No Content`:** (sem corpo)

**Resposta `404 Not Found`:**
```json
{
  "error": "Tarefa não encontrada"
}
```

---

## 📖 Documentação Swagger

**Pasta:** `docs/`

A documentação da API é escrita no formato **OpenAPI 3.0** no arquivo `docs/swagger.yaml`. Ela é servida automaticamente pelo **Swagger UI** na rota `/docs`.

A especificação define:

- **Paths:** Todos os endpoints disponíveis com seus métodos HTTP
- **Schemas:** Estrutura dos objetos de entrada e saída (`User`, `UserInput`, `Task`, `TaskInput`, `TaskUpdate`)
- **Responses:** Códigos de status possíveis para cada endpoint
- **Tags:** Agrupamento dos endpoints em "Usuários" e "Tarefas"

Para acessar a documentação interativa, inicie o servidor e acesse:

```
http://localhost:5000/docs
```

Na interface Swagger, é possível testar os endpoints diretamente pelo navegador.

---

## 🖥 Interface Web (Front-end)

**Pasta:** `templates/`

O projeto inclui uma interface web simples em `templates/index.html`, construída com **Bootstrap 5** e **JavaScript puro** (Fetch API). A interface permite:

- **Cadastrar usuários** através de um formulário
- **Visualizar a lista de usuários** cadastrados
- **Criar tarefas** selecionando o usuário responsável
- **Editar tarefas** através de um modal
- **Marcar tarefas como concluídas**
- **Excluir tarefas** com confirmação

A interface consome os endpoints da própria API via requisições AJAX, demonstrando o funcionamento completo do sistema.

**Acesso:** `http://localhost:5000`

---

## 🗄 Banco de Dados

O projeto utiliza **SQLite** por padrão, armazenando os dados no arquivo `tasks.db` na raiz do projeto. As tabelas são criadas automaticamente ao executar `app.py`.

### Diagrama de Entidade-Relacionamento

```
┌──────────────┐          ┌──────────────────┐
│    users     │          │      tasks       │
├──────────────┤          ├──────────────────┤
│ id (PK)      │──┐       │ id (PK)          │
│ name         │  │       │ title            │
│ email        │  └──────►│ user_id (FK)     │
│              │   1   N  │ description      │
│              │          │ completed        │
└──────────────┘          └──────────────────┘
```

### Configuração

A string de conexão é definida em `config.py` e pode ser alterada via variável de ambiente `DATABASE_URL`:

```python
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
```

Para usar outro banco (ex.: PostgreSQL), basta definir a variável:

```bash
set DATABASE_URL=postgresql://user:pass@localhost/taskdb
python app.py
```
