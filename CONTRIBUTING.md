# Guia de Contribuicao

## Fluxo de branches
- `main`: branch de produção.
- `develop`: branch de integração contínua (recomendado criar no repositório remoto).
- `feat/*`: novas funcionalidades.
- `fix/*`: correções.
- `chore/*`: manutenção técnica.

## Fluxo de pull request
1. Crie branch a partir de `develop` (ou `main` quando `develop` não existir).
2. Faça commits descritivos e pequenos.
3. Abra PR usando o template.
4. Aguarde CI verde.
5. Revisão de código obrigatória.
6. Merge com squash para manter histórico limpo.

## Critérios de aprovação
- CI aprovado.
- Testes cobrindo mudança principal.
- Sem regressão de permissões ou segurança.
- README/docs atualizados quando aplicável.

## Padrão de commit
Use mensagens no imperativo, por exemplo:
- `Add category filter in post list`
- `Fix permission check in admin edit`
- `Update CI workflow for migration check`
