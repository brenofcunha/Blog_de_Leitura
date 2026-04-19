# Decisões Técnicas

## Banco de dados
- PostgreSQL como alvo principal.
- SQLite como fallback local para desenvolvimento rápido.

## Permissões
- Regra centralizada em service para evitar duplicação em views.

## Renderização de conteúdo
- Suporte básico de Markdown no backend para leitura.

## Qualidade
- CI com lint, format check, migration check e testes.
- Meta de cobertura mínima via pytest-cov.
