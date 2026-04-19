# Fluxo de Dados

## Fluxo de post
1. Autor autenticado cria/edita post no admin.
2. Formulário valida dados obrigatórios.
3. Service/repository persistem no banco.
4. Se status = publicado, post entra no portal público.
5. Área pública consulta apenas posts publicados.

## Fluxo de usuário
1. Usuário faz login em `/login`.
2. Após autenticação, redireciona para painel.
3. Permissões determinam escopo de gerenciamento.

## Fluxo de leitura
1. Visitante acessa `/` ou `/posts/`.
2. Pode usar busca/filtros por categoria/tag.
3. Abre detalhe por slug em `/posts/<slug>/`.
