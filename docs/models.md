# Modelos e Banco de Dados

## Visao geral

O dominio principal gira em torno de usuarios e publicacao de posts.
As entidades centrais sao:

- User (Django auth)
- UserProfile
- Post
- Category
- Tag

## Entidades

### User

Entidade nativa do Django para autenticacao e identidade.
Campos relevantes no contexto do projeto:

- username
- password (hash)
- is_staff
- is_superuser
- is_active

### UserProfile

Complementa o User com papel de negocio.

Campos:

- user (OneToOne com User)
- role: admin ou autor

Regra:

- user staff/superuser e tratado como admin no sistema

### Post

Representa conteudo editorial.

Campos principais:

- title: titulo do post
- slug: identificador amigavel para URL
- summary: resumo curto
- content: conteudo do post
- cover_image: imagem opcional de capa
- status: rascunho ou publicado
- author: autor do post (FK para User)
- categories: categorias relacionadas (M2M)
- tags: tags relacionadas (M2M)
- created_at / updated_at
- published_at

Regras de negocio:

- slug e gerado automaticamente se estiver vazio
- se status mudar para publicado e published_at for nulo, published_at recebe data/hora atual
- se status voltar para rascunho, published_at volta para nulo

### Category

Classifica posts por tema macro.

Campos:

- name (unico)
- slug (unico)

Regra:

- slug e gerado automaticamente a partir de name

### Tag

Classifica posts por marcador especifico.

Campos:

- name (unico)
- slug (unico)

Regra:

- slug e gerado automaticamente a partir de name

## Relacionamentos

- User 1:N Post
- User 1:1 UserProfile
- Post N:N Category
- Post N:N Tag

Resumo textual:

User ---< Post >--- Category
  |           \
  |            >--- Tag
  >--- UserProfile

## Indices e performance

Indices definidos em Post:

- status + published_at (listagem publica)
- author + status (painel do autor/admin)
- slug unico e indexado (detalhe publico)

Beneficio pratico:

- melhora consulta de listagens publicas e administrativas
- reduz custo de busca por slug

## Regras de status do post

- rascunho: visivel somente no contexto administrativo
- publicado: visivel no portal publico

Exemplo pratico:

1. autor cria post e salva como rascunho
2. post nao aparece em / nem em /posts/
3. autor publica o post
4. post passa a aparecer na area publica

## Validacoes relevantes

Validacoes de formulario para Post:

- title obrigatorio
- content obrigatorio
- cover_image apenas jpg, jpeg, png e webp

Validacoes de model/regras:

- slug unico por post
- status controla published_at

## Observacoes de manutencao

- alteracoes em regras de status devem ser refletidas em models.py e docs/flows.md
- alteracoes de permissao devem ser refletidas em services e docs/permissions.md
