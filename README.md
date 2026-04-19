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
- Vercel (deploy serverless)
- django-storages + Amazon S3 (uploads em produção)

## Settings por ambiente

O projeto usa módulos separados de configuração:
- `config.settings.base`
- `config.settings.development`
- `config.settings.production`

Padrão local:
- `manage.py` e `pytest` usam `config.settings.development`

Deploy (WSGI/ASGI):
- padrão em produção: `config.settings.production`

Variável principal:

```bash
DJANGO_SETTINGS_MODULE=config.settings.development
# ou
DJANGO_SETTINGS_MODULE=config.settings.production
```

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

Para produção, as variáveis abaixo são obrigatórias:

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS` (separado por vírgula)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (separado por vírgula e com `https://`)
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Exemplo de produção:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=<segredo-forte>
DJANGO_ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://seudominio.com,https://www.seudominio.com
POSTGRES_DB=blog_leitura
POSTGRES_USER=blog_user
POSTGRES_PASSWORD=<senha-forte>
POSTGRES_HOST=<host-postgres>
POSTGRES_PORT=5432
AWS_STORAGE_BUCKET_NAME=<bucket>
AWS_S3_REGION_NAME=us-east-1
AWS_ACCESS_KEY_ID=<access-key>
AWS_SECRET_ACCESS_KEY=<secret-key>
# opcional
AWS_S3_CUSTOM_DOMAIN=cdn.seudominio.com
```

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

Para forçar execução local com settings explícito:

```bash
# Windows PowerShell
$env:DJANGO_SETTINGS_MODULE="config.settings.development"
python manage.py runserver
```

Aplicação:
- público: `http://127.0.0.1:8000/`
- admin django: `http://127.0.0.1:8000/django-admin/`

## Deploy Vercel (Static + Media)

### Arquivos estáticos

- `STATIC_ROOT` foi definido para `staticfiles/`.
- O build do Vercel executa automaticamente:

```bash
python manage.py collectstatic --noinput
```

- O roteamento está configurado em `vercel.json` para servir `/static/*` a partir de `staticfiles/*`.

### Uploads em produção

- Em desenvolvimento, uploads continuam locais (`MEDIA_ROOT`).
- Em produção, uploads usam storage externo S3 via `django-storages`.
- O Django não depende de disco local no Vercel para mídia em produção.

### Variáveis no painel da Vercel

Configure no projeto Vercel:

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_CUSTOM_DOMAIN` (opcional)

Nunca versione credenciais reais no repositório.

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
