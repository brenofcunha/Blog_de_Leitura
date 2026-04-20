# Fluxos de Negocio

## Objetivo

Descrever os fluxos de posts para facilitar manutencao e evolucao sem quebra de comportamento.

## Fluxo 1: Criacao de post

Pre-condicoes:

- usuario autenticado
- acesso ao painel administrativo

Passo a passo:

1. usuario acessa /admin/posts/novo
2. preenche formulario (titulo, resumo, conteudo, categorias, tags, imagem)
3. escolhe acao no submit:
   - save_draft
   - publish
4. backend valida dados no PostForm
5. controller define author com usuario autenticado
6. controller ajusta status conforme action
7. repository salva post
8. sistema redireciona para /admin/posts

Validacoes envolvidas:

- titulo obrigatorio
- conteudo obrigatorio
- formato de imagem permitido (jpg, jpeg, png, webp)

## Fluxo 2: Salvar como rascunho

Regra central:

- status do post = rascunho
- post nao aparece na area publica
- published_at deve ficar nulo

Exemplo:

- acao submit: save_draft
- resultado: post visivel apenas em rotas administrativas

## Fluxo 3: Publicacao

Regra central:

- status do post = publicado
- post passa a aparecer nas consultas publicas
- published_at e preenchido automaticamente no model quando necessario

Exemplo:

- acao submit: publish
- resultado: post passa a aparecer em / e /posts/

## Fluxo 4: Edicao de post

Pre-condicoes:

- usuario autenticado
- usuario com permissao para gerenciar o post

Passo a passo:

1. usuario acessa /admin/posts/{id}/editar
2. backend recupera post por id
3. service valida permissao (can_manage_post)
4. usuario envia alteracoes
5. PostForm valida dados
6. controller aplica mudanca de status conforme action
7. repository salva alteracoes

Comportamento esperado:

- autor edita apenas posts proprios
- admin pode editar qualquer post

## Fluxo 5: Exclusao de post

Pre-condicoes:

- metodo HTTP deve ser POST
- usuario autenticado
- usuario com permissao no post

Passo a passo:

1. usuario envia POST para /admin/posts/{id}/excluir
2. backend valida permissao
3. repository remove registro
4. sistema redireciona para /admin/posts

## Fluxo de leitura publica

1. visitante acessa /
2. sistema exibe destaque e lista de posts publicados
3. visitante acessa /posts/ para lista completa
4. filtros opcionais:
   - q para busca textual
   - categoria por slug
   - tag por slug
5. visitante abre /posts/{slug}/ para detalhe

## Regras de status e visibilidade

- apenas posts publicados entram em listagens publicas
- post em rascunho retorna 404 no detalhe publico por slug

## Exemplos praticos de requisicao

Exemplo de busca publica:

GET /posts/?q=django

Exemplo de filtro por categoria:

GET /posts/?categoria=backend

Exemplo de filtro por tag:

GET /posts/?tag=python

Exemplo de publicacao no painel:

POST /admin/posts/novo
Campos principais: title, summary, content, action=publish
