# Arquitetura do Sistema

## Visão geral
O projeto usa Django com separação por camadas:
- controllers: recebem requests e montam contexto de resposta
- services: regras de negócio e autorização
- repositories: consultas e filtros de dados
- templates/static: interface pública e administrativa

## Componentes principais
- Área pública: home, listagem, detalhe por slug
- Área administrativa: dashboard, CRUD de posts
- Autenticação: login/logout do Django
- Permissões: autor x admin

## Princípios aplicados
- Views leves, sem regra complexa
- Regras de permissão centralizadas em service
- Consultas reutilizáveis no repository
- Evolução incremental por etapas
