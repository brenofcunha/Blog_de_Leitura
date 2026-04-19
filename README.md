# Blog de Leitura

Portal de posts com Django, foco editorial e experiência completa para leitura e gestão de conteúdo.

## Objetivo do sistema

Oferecer uma plataforma com:
- área pública para leitura de posts publicados
- área administrativa para criação e edição de conteúdo
- controle de permissões entre autores e administradores
- base técnica para evolução contínua com qualidade e CI/CD

## Funcionalidades principais

- autenticação com login/logout
- CRUD de posts no painel administrativo
- status de post: rascunho e publicado
- busca pública por título/resumo/conteúdo
- filtros por categoria e tag
- paginação na listagem pública
- navegação entre posts e sugestões de leitura
- upload de imagem de capa
- testes automatizados e pipeline de CI

## Tecnologias utilizadas

- Python 3.13
- Django 5
- PostgreSQL (alvo principal)
- SQLite (fallback para desenvolvimento)
- Pytest, pytest-django, pytest-cov
- Black, isort, flake8
- GitHub Actions

## Instalação

### 1. Clonar repositório

```bash
git clone https://github.com/brenofcunha/Blog_de_Leitura.git
cd Blog_de_Leitura
```

### 2. Configurar ambiente

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. Configurar variáveis

Copie `.env.example` para `.env` e ajuste valores.

Exemplo mínimo para PostgreSQL:

```bash
USE_POSTGRES=1
POSTGRES_DB=blog_leitura
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Se `USE_POSTGRES` for diferente de `1`, o projeto usa SQLite local.

### 4. Instalar dependências e subir banco

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

## Execução

```bash
python manage.py runserver
```

Aplicação:
- público: `http://127.0.0.1:8000/`
- admin django: `http://127.0.0.1:8000/django-admin/`

## Qualidade e testes

```bash
python -m pip install -r requirements-dev.txt
python manage.py test
black --check .
isort --check-only .
flake8 .
pytest
```

## Estrutura do projeto

```text
config/
leitura/
  controllers/
  services/
  repositories/
  routes/
  templates/
  static/
docs/
.github/
scripts/
```

## Rotas principais

- `/`
- `/posts/`
- `/posts/<slug>/`
- `/login`
- `/admin`
- `/admin/posts`
- `/admin/posts/novo`
- `/admin/posts/<id>/editar`
- `/admin/posts/<id>/excluir`

## Documentação técnica

- `docs/architecture.md`
- `docs/data-flow.md`
- `docs/database-model.md`
- `docs/technical-decisions.md`
- `docs/coding-standards.md`
- `docs/github-setup.md`
- `docs/manual-tests.md`
- `docs/portfolio.md`

## Roadmap (Etapas 1 a 10)

- Etapa 1: organização da base e separação público/admin
- Etapa 2: CRUD com persistência em banco
- Etapa 3: portal público dinâmico
- Etapa 4: evolução editorial e gestão
- Etapa 5: UX avançada e descoberta de conteúdo
- Etapa 6: segurança e robustez operacional
- Etapa 7: qualidade de código, testes e CI/CD
- Etapa 8: observabilidade e métricas de uso
- Etapa 9: produto, documentação e experiência de projeto
- Etapa 10: preparação final para portfólio e release

## Contribuição

Leia `CONTRIBUTING.md` para fluxo de branches, PRs e critérios de aprovação.
