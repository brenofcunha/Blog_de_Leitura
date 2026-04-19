# Testes Manuais Criticos

## Autenticacao
- Login com usuario valido.
- Logout e retorno para area publica.
- Tentativa de acessar `/admin` sem login redireciona para `/login`.

## Fluxo de Conteudo
- Criar post em rascunho.
- Editar post antigo.
- Publicar post e validar exibicao publica.

## Permissoes
- Autor A nao consegue editar/excluir post do Autor B.
- Admin consegue editar/excluir qualquer post.

## Area Publica
- Busca por titulo retorna resultados esperados.
- Filtro por categoria e tag funciona corretamente.
- Paginacao navega entre paginas sem perder filtros.
- Detalhe por slug retorna 404 para post inexistente e rascunho.
