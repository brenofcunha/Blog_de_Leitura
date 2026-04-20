# Arquitetura do Sistema

## Visao geral

O projeto segue o padrao Django com separacao por camadas para facilitar manutencao, testes e evolucao:

- routes: define caminhos HTTP e nomes das rotas
- controllers: trata request/response e prepara contexto para templates
- services: concentra regras de negocio e autorizacao
- repositories: centraliza consultas e filtros no banco
- models: define entidades e comportamento de persistencia

Essa separacao evita regra de negocio espalhada em views e reduz risco de regressao ao evoluir funcionalidades.

## Estrutura de pastas relevante

- config/: configuracoes globais, settings por ambiente e urls principais
- leitura/routes/: composicao de rotas publicas, administrativas e autenticacao
- leitura/controllers/: entradas da aplicacao (public, admin, auth)
- leitura/services/: regras de dominio (ex.: permissao de gerenciamento)
- leitura/repositories/: acesso a dados e filtros de consulta
- leitura/models.py: entidades UserProfile, Post, Category e Tag
- leitura/forms.py: validacoes de formulario e input de post

## Fluxo de requisicao (request -> response)

### Exemplo 1: listagem publica de posts

1. Cliente chama GET /posts/?q=django&categoria=backend
2. route public_urls.py mapeia para public_views.post_list
3. controller coleta filtros da query string
4. service chama published_posts
5. repository aplica filtros no banco e retorna QuerySet
6. controller pagina e renderiza template views/public/post_list.html
7. cliente recebe HTML com posts publicados

### Exemplo 2: edicao de post no admin

1. Usuario autenticado chama POST /admin/posts/{id}/editar
2. route admin_urls.py mapeia para admin_views.admin_post_edit
3. controller busca post e valida permissao com can_manage_post
4. form valida campos obrigatorios e arquivo de capa
5. controller ajusta status conforme action (publish/save_draft)
6. repository persiste alteracoes
7. response redireciona para /admin/posts

## Mapa de rotas

### Rotas publicas

- /
- /posts/
- /posts/{slug}/

### Rotas administrativas

- /admin
- /admin/posts
- /admin/posts/novo
- /admin/posts/{id}/editar
- /admin/posts/{id}/excluir

### Rotas de autenticacao

- /login
- /logout
- /pos-login

### Rota do Django Admin nativo

- /django-admin/

## Decisoes tecnicas

### Por que Django

- framework robusto, maduro e com recursos nativos de autenticacao, ORM e seguranca
- acelera entrega de funcionalidades sem perder padronizacao

### Por que PostgreSQL

- confiavel para ambiente de producao
- bom suporte a indices e consultas relacionais do dominio (Post, Category, Tag)
- aderente ao ecossistema Django

### Por que services + repositories

- services: evita repeticao de regras de permissao em varios controllers
- repositories: evita duplicacao de filtros/queries e simplifica manutencao
- juntos: melhor separacao de responsabilidade e menor acoplamento

### Decisoes de design importantes

- status de post como rascunho/publicado para separar edicao interna de publicacao
- publicacao controla published_at automaticamente no model
- listagem publica retorna somente posts publicados
- permissao em camada de service para garantir consistencia entre endpoints

## Seguranca e operacao (visao arquitetural)

- settings separados por ambiente: base, development, production
- producao exige variaveis obrigatorias de seguranca (secret key, hosts, CSRF trusted origins)
- cookies seguros e redirecionamento HTTPS configurados em producao
- static e media separados: staticfiles para build, S3 para uploads em producao

## Como usar este documento

- novo no projeto: ler este arquivo antes de alterar codigo
- mudanca em regra de negocio: revisar tambem docs/flows.md e docs/permissions.md
- mudanca de infraestrutura: revisar docs/deployment.md
