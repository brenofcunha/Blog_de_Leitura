# Modelo de Banco de Dados

Este documento foi mantido por compatibilidade historica.

Versao completa e atualizada:

- docs/models.md

Resumo rapido:

- entidades: User, UserProfile, Post, Category, Tag
- post possui status rascunho/publicado
- published_at segue regra de status no model
- indices principais em Post:
  - status + published_at
  - author + status
  - slug unico/indexado
