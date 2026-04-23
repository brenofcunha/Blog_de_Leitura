# Blog de Leitura

Portal de posts multiusuario construido com Django, com area publica para leitura e area administrativa para autores e administradores.

## Objetivo do sistema

O Blog de Leitura existe para permitir que multiplos autores publiquem conteudo de forma organizada, com regras claras de permissao e um fluxo editorial simples:

- criar conteudo
- salvar como rascunho
- publicar quando estiver pronto
- editar e excluir com seguranca

## Funcionalidades principais

- autenticacao com login/logout
- painel administrativo para autores e admins
- CRUD de posts com status rascunho/publicado
- busca publica por titulo, resumo e conteudo
- filtros por categoria e tag
- paginacao da lista publica
- navegacao entre posts e sugestoes de leitura
- upload de imagem de capa
- testes automatizados com Django TestCase e Pytest

## Stack tecnologica

- Python 3.13
- Django 5.2
- SQLite (desenvolvimento padrao)
- PostgreSQL ou MySQL em producao (por variavel de ambiente)
- django-storages + boto3 (S3 opcional para uploads em producao)
- pytest, pytest-django, pytest-cov
- black, isort, flake8
- HostGator (cPanel/Passenger ou VPS)

## Arquitetura em alto nivel

O projeto usa separacao por camadas para manter responsabilidades claras:

- routes: definicao de rotas HTTP
- controllers: entrada de requests e retorno de responses
- services: regras de negocio e autorizacao
- repositories: consultas e persistencia
- models: entidades e relacoes de banco

Fluxo padrao de requisicao:

request -> route -> controller -> service -> repository/model -> response

Documentacao detalhada:

- docs/architecture.md
- docs/models.md
- docs/flows.md
- docs/permissions.md
- docs/deployment.md

## Como rodar localmente

### 1. Clonar o repositorio

Comando:

git clone [https://github.com/brenofcunha/Blog_de_Leitura.git](https://github.com/brenofcunha/Blog_de_Leitura.git)

Entrar na pasta:

cd Blog_de_Leitura

### 2. Criar e ativar ambiente virtual

Windows (cmd/PowerShell):

python -m venv .venv
.venv\Scripts\activate

Linux/macOS:

python -m venv .venv
source .venv/bin/activate

### 3. Instalar dependencias

python -m pip install -r requirements.txt

### 4. Configurar variaveis de ambiente

Use o arquivo .env.example como base e crie o seu .env.

Ambiente local com SQLite (mais simples):

DJANGO_SETTINGS_MODULE=config.settings.development
DATABASE_ENGINE=sqlite

Ambiente local com PostgreSQL:

DJANGO_SETTINGS_MODULE=config.settings.development
DATABASE_ENGINE=postgresql
POSTGRES_DB=blog_leitura
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

### 5. Aplicar migracoes

python manage.py migrate

### 6. Validar projeto

python manage.py check

### 7. Executar servidor

python manage.py runserver

URLs principais:

- publico: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- admin Django nativo: [http://127.0.0.1:8000/django-admin/](http://127.0.0.1:8000/django-admin/)
- painel administrativo da aplicacao: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Rotas do sistema

### Publicas

- /
- /posts/
- /posts/{slug}/

Exemplo de filtros:

- /posts/?q=django
- /posts/?categoria=backend
- /posts/?tag=python

### Administrativas

- /admin
- /admin/posts
- /admin/posts/novo
- /admin/posts/{id}/editar
- /admin/posts/{id}/excluir

### Autenticacao

- /login
- /logout

## Regras de permissao (resumo)

- Admin (is_staff/is_superuser) pode gerenciar qualquer post
- Autor gerencia apenas os proprios posts
- Usuario nao autenticado nao acessa area administrativa

Detalhes completos em docs/permissions.md.

## Qualidade, testes e manutencao segura

Instalar ferramentas de desenvolvimento:

python -m pip install -r requirements-dev.txt

Validacoes recomendadas antes de abrir PR:

- python manage.py check
- python manage.py test
- pytest
- black --check .
- isort --check-only .
- flake8 .

## Deploy e operacao

Resumo:

- producao usa config.settings.production
- banco configuravel por variavel: MySQL ou PostgreSQL
- arquivos estaticos: collectstatic para staticfiles/
- uploads de midia: S3 (opcional) ou local seguro

Guia completo em docs/deployment.md.

## Seguranca pre-producao (obrigatorio)

Antes de publicar em ambiente aberto, configure obrigatoriamente:

- DEBUG=0 em producao
- SECRET_KEY (ou DJANGO_SECRET_KEY) sem fallback no codigo
- ALLOWED_HOSTS (ou DJANGO_ALLOWED_HOSTS) com dominios explicitos
- CSRF_TRUSTED_ORIGINS (ou DJANGO_CSRF_TRUSTED_ORIGINS) com https://

Configuracoes de seguranca ativas em producao:

- SESSION_COOKIE_SECURE=True
- CSRF_COOKIE_SECURE=True
- SECURE_SSL_REDIRECT=True (por padrao)
- SECURE_HSTS_SECONDS configurado
- SECURE_HSTS_INCLUDE_SUBDOMAINS=True
- SECURE_HSTS_PRELOAD=True
- SECURE_CONTENT_TYPE_NOSNIFF=True
- X_FRAME_OPTIONS=DENY

Regras importantes:

- a aplicacao falha se SECRET_KEY nao estiver definida
- a aplicacao falha se ALLOWED_HOSTS estiver vazio ou com "*"
- a aplicacao falha se CSRF_TRUSTED_ORIGINS nao estiver definido corretamente
- em producao, DEBUG=True e bloqueado na inicializacao

Exemplo minimo de variaveis para producao:

```env
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=0
SECRET_KEY=troque-por-uma-chave-forte
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
CSRF_TRUSTED_ORIGINS=https://seudominio.com,https://www.seudominio.com
DATABASE_ENGINE=mysql
MYSQL_DATABASE=blog_leitura
MYSQL_USER=blog_user
MYSQL_PASSWORD=senha-forte
MYSQL_HOST=host-do-banco
MYSQL_PORT=3306
```

Checklist rapido de validacao:

1. sistema sobe com DEBUG=0
2. sistema falha sem SECRET_KEY
3. host fora de ALLOWED_HOSTS nao e aceito
4. formularios funcionam com CSRF_TRUSTED_ORIGINS correto
5. cookies possuem flag Secure
6. HTTP e redirecionado para HTTPS
7. erros nao exibem stack trace para usuario final

## Estrutura resumida do projeto

config/
leitura/
  controllers/
  services/
  repositories/
  routes/
  models.py
  forms.py
  templates/
  static/
docs/
scripts/

## Roadmap

- curto prazo: melhorar observabilidade, cobertura de testes e diagnostico de falhas
- medio prazo: evoluir UX editorial e automacao de revisao de conteudo
- longo prazo: ampliar funcionalidades de colaboracao e analytics para autores

## Onboarding rapido para novos devs

1. Rodar o passo a passo de instalacao acima
2. Ler docs/architecture.md para entender o desenho tecnico
3. Ler docs/flows.md e docs/permissions.md antes de alterar regra de negocio
4. Validar alteracoes com testes e lint

## Contribuicao

Leia CONTRIBUTING.md para fluxo de branches, convencoes de commit e criterios de revisao.
