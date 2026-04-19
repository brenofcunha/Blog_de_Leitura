# Modelo de Banco de Dados

## Entidades principais
- User (Django auth)
- UserProfile (papel admin/autor)
- Post
- Category
- Tag

## Post
Campos relevantes:
- title, slug, summary, content
- status (rascunho/publicado)
- author (FK)
- categories (M2M)
- tags (M2M)
- cover_image
- created_at, updated_at, published_at

## Índices
- status + published_at
- author + status
- slug único

Esses índices melhoram busca e listagens públicas.
