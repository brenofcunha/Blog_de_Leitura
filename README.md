# Blog_de_Leitura

Portal de posts em Django com separacao entre area publica e area administrativa.

## Como rodar localmente

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Usando PostgreSQL

Defina as variaveis de ambiente antes de subir o servidor:

```bash
USE_POSTGRES=1
POSTGRES_DB=blog_leitura
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Se `USE_POSTGRES` nao estiver igual a `1`, o projeto usa SQLite como fallback local.

## Etapa 1 implementada

- Area publica para leitura de posts publicados.
- Area administrativa para criar e editar posts.
- Autenticacao com login/logout.
- Controle de acesso por autor e admin.
- Separacao entre posts em rascunho e publicados.
- Limite de ate 5 usuarios ativos no portal.

## Etapa 2 implementada

- Integracao com PostgreSQL por variaveis de ambiente.
- Camada de acesso a dados centralizada em `leitura/repositories`.
- CRUD de posts no painel administrativo.
- Filtros de listagem por status e titulo.
- Acao de salvar rascunho e publicar no formulario.
- Controle de permissao no backend (autor/admin).
- Campo `published_at` para registrar publicacao.
- Testes dos fluxos essenciais da interface de posts.

## Rotas

### Publicas

- `/`
- `/posts`
- `/posts/<slug>`

### Administrativas

- `/login`
- `/admin`
- `/admin/posts`
- `/admin/posts/novo`
- `/admin/posts/<id>/editar`
- `/admin/posts/<id>/excluir`

### Admin do Django

- `/django-admin/`

## Estrutura aplicada

```text
leitura/
	controllers/
	services/
	routes/
	repositories/
	templates/
		views/
			public/
			admin/
```

## Modelo de dados

- `Post`: titulo, slug, resumo, conteudo, status (rascunho/publicado), autor, created_at, updated_at, published_at.
- `UserProfile`: papel (admin/autor) ligado ao usuario autenticado do Django.
