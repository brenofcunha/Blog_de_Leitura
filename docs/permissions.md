# Permissoes e Controle de Acesso

## Perfis do sistema

### Admin

Identificacao:

- usuario com is_staff=True ou is_superuser=True
- ou perfil de negocio com role=admin

Capacidades:

- criar post
- editar qualquer post
- excluir qualquer post
- visualizar todos os posts no painel

### Autor

Identificacao:

- usuario autenticado sem privilegio de staff/superuser
- role padrao: autor

Capacidades:

- criar post
- editar apenas os proprios posts
- excluir apenas os proprios posts
- visualizar no painel apenas os proprios posts

## Regras por acao

### Criar

- permitido para usuario autenticado
- autor do post sempre e o usuario logado

### Editar

- permitido se usuario for admin
- permitido se usuario for autor do post
- negado (403) para outros autores

### Excluir

- permitido se usuario for admin
- permitido se usuario for autor do post
- negado (403) para outros autores
- endpoint exige POST

### Listar no painel

- admin lista todos os posts
- autor lista apenas os proprios posts

## Onde as permissoes sao aplicadas

### Backend

- controllers admin usam login_required
- controllers admin chamam can_manage_post antes de editar/excluir
- service can_manage_everything centraliza regra de escopo global
- repository list_for_user aplica filtro por autor para nao-admin

### Camadas envolvidas

- controllers: barram acesso e retornam 403 quando necessario
- services: determinam se pode gerenciar
- repositories: restringem visibilidade de dados

## Exemplos praticos

### Cenário 1: autor tenta editar post de outro autor

- requisicao: POST /admin/posts/{id}/editar
- resultado esperado: 403 PermissionDenied

### Cenário 2: admin edita post de qualquer autor

- requisicao: POST /admin/posts/{id}/editar
- resultado esperado: 302 redirect para /admin/posts

### Cenário 3: usuario nao autenticado acessa painel

- requisicao: GET /admin
- resultado esperado: redirecionamento para login

## Boas praticas para evolucao

- toda nova regra de permissao deve ser adicionada primeiro em service
- evitar logica de autorizacao duplicada em templates
- cobrir alteracoes de permissao com testes de integracao/controlador
