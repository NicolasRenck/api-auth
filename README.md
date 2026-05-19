# API de Autenticação

API REST para autenticação e gerenciamento de usuários, com JWT, controle de acesso, log de acessos e troca de senha.

Desenvolvida com **Django** e **Django REST Framework**.

## Deploy

- **API:** https://api-auth-bqyh.onrender.com
- **Docs (Swagger):** https://api-auth-bqyh.onrender.com/api/docs/

---

## Tecnologias

- Python 3.13
- Django 6.0
- Django REST Framework
- PostgreSQL
- SimpleJWT - autenticação via token
- drf-spectacular - documentação automática (Swagger)
- Docker + Docker Compose

---

## Como rodar localmente

### Com Docker (recomendado)

**Pré-requisitos:** Docker e Docker Compose instalados.

```bash
# Clone o repositório
git clone https://github.com/NicolasRenck/api-auth.git
cd api-auth

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Suba os containers
docker compose up --build

# Em outro terminal, rode as migrations
docker compose exec web python manage.py migrate

# (Opcional) Crie um superusuário
docker compose exec web python manage.py createsuperuser
```

A API estará disponível em `http://localhost:8000`.

### Sem Docker

**Pré-requisitos:** Python 3.13+ e PostgreSQL instalados.

```bash
git clone https://github.com/NicolasRenck/api-auth.git
cd api-auth

python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

cp .env.example .env
# Edite o .env com as credenciais do seu banco

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Autenticação

A API utiliza **JWT (JSON Web Token)**. Para acessar os endpoints protegidos, inclua o token no header de cada requisição.

### Obtendo o token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

### Usando o token

```http
Authorization: Bearer <seu_access_token>
```

### Renovando o token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "seu_refresh_token"
}
```

---

## Endpoints

### Autenticação e Usuário

| Método | Endpoint | Autenticação | Descrição |
|--------|----------|:---:|-----------|
| `POST` | `/api/register/` | ❌ | Cria um novo usuário |
| `POST` | `/api/token/` | ❌ | Obtém access e refresh token |
| `POST` | `/api/token/refresh/` | ❌ | Renova o access token |
| `POST` | `/api/logout/` | ✅ | Invalida o refresh token (blacklist) |
| `GET` | `/api/me/` | ✅ | Retorna os dados do usuário autenticado |
| `PATCH` | `/api/me/` | ✅ | Atualiza os dados do usuário autenticado |
| `POST` | `/api/change-password/` | ✅ | Altera a senha do usuário autenticado |

### Log de Acessos

| Método | Endpoint | Autenticação | Descrição |
|--------|----------|:---:|-----------|
| `GET` | `/api/log-acesso/` | ✅ | Lista o histórico de acessos do usuário |
| `GET` | `/api/log-acesso/{id}/` | ✅ | Detalha um registro de acesso específico |

---

## Documentação interativa

Com o projeto rodando, acesse:

```
http://localhost:8000/api/docs/
```

Interface Swagger com todos os endpoints documentados e testáveis.

---

## Estrutura do projeto

```
api-auth/
├── app/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── requirements.txt
```

---

## Segurança

Cada usuário tem acesso **apenas aos seus próprios dados**. Logs de acesso, dados de perfil e alterações de senha são sempre filtrados pelo usuário autenticado, não é possível acessar ou modificar informações de outros usuários.

---

## Como testar

1. Crie um usuário em `POST /api/register/`
2. Obtenha o token em `POST /api/token/`
3. Use o token no header: `Authorization: Bearer seu_token`
4. Explore os demais endpoints autenticados

---

## Autor

**Nicolas Renck**  
[github.com/NicolasRenck](https://github.com/NicolasRenck)