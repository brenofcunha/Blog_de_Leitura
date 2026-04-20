# 📌 roteiro.md — Implementação de Banco em Produção

**Stack:** Django + PostgreSQL (Railway) + Deploy (Vercel)
**Objetivo:** Executar as etapas de forma guiada, usando um agente de desenvolvimento.

---

# 🧭 Como usar este roteiro

Para cada etapa:

1. Copie o **prompt da etapa**
2. Envie para o agente
3. Revise o resultado
4. Só avance quando estiver validado

---

# 🚀 Etapa 1 — Separar ambientes

## Prompt

Implemente a separação de ambientes no projeto Django:

* Criar estrutura:
  config/settings/base.py
  config/settings/development.py
  config/settings/production.py

* base.py → configs comuns

* development.py → DEBUG=True

* production.py → DEBUG=False + segurança

* Configurar DJANGO_SETTINGS_MODULE via variável de ambiente

* Garantir:

  * produção falha sem SECRET_KEY
  * nenhum segredo hardcoded

* Criar `.env.example`

---

# 🚀 Etapa 2 — Criar banco PostgreSQL no Railway

## Prompt

Configure o banco de dados em produção usando Railway:

* Criar serviço PostgreSQL no Railway

* Identificar variáveis:

  * DATABASE_URL ou PGHOST, PGUSER, etc

* Documentar conexão

* Garantir que banco está acessível externamente

---

# 🚀 Etapa 3 — Conectar Django ao Railway

## Prompt

Configure o Django para usar PostgreSQL em produção:

* Remover uso de SQLite em produção
* Usar DATABASE_URL ou variáveis do Railway
* Configurar conexão no settings de produção
* Garantir:

  * falha se banco não estiver configurado
  * conexão segura funcionando

---

# 🚀 Etapa 4 — Configurar variáveis no Vercel

## Prompt

Configure as variáveis de ambiente no Vercel:

* Adicionar:

  * DATABASE_URL
  * SECRET_KEY
  * DEBUG=False
  * ALLOWED_HOSTS
  * CSRF_TRUSTED_ORIGINS

* Garantir que a aplicação usa essas variáveis

* Testar build e deploy

---

# 🚀 Etapa 5 — Testar conexão Vercel → Railway

## Prompt

Valide a conexão entre Django (Vercel) e PostgreSQL (Railway):

* Testar queries simples
* Verificar erros de conexão
* Validar latência básica
* Garantir que aplicação responde corretamente

---

# 🚀 Etapa 6 — Rodar migrations em produção

## Prompt

Configure e execute migrations em produção:

* Rodar:
  python manage.py migrate

* Garantir:

  * tabelas criadas corretamente
  * sem erros de schema
  * banco consistente

---

# 🚀 Etapa 7 — Criar usuário admin e dados iniciais

## Prompt

Prepare o banco para uso inicial:

* Criar superusuário

* Inserir dados iniciais:

  * categorias
  * tags

* Validar acesso ao admin

* Garantir que sistema não está vazio

---

# 🚀 Etapa 8 — Revisar schema e integridade

## Prompt

Revise o banco de dados para produção:

* Validar:

  * índices
  * slug único
  * relacionamentos
  * constraints

* Corrigir possíveis inconsistências

* Garantir integridade dos dados

---

# 🚀 Etapa 9 — Configurar backup

## Prompt

Implemente estratégia de backup no Railway:

* Ativar backups automáticos
* Definir frequência
* Documentar processo
* Testar restauração

---

# 🚀 Etapa 10 — Monitoramento do banco

## Prompt

Implemente monitoramento básico do PostgreSQL:

* Monitorar:

  * conexões
  * uso de recursos
  * erros

* Preparar base para observabilidade futura

---

# 🚀 Etapa 11 — Documentação

## Prompt

Atualize a documentação do projeto:

* Explicar:

  * conexão com Railway
  * variáveis de ambiente
  * deploy no Vercel
  * migrations
  * backup

* Atualizar README

* Criar docs/ se necessário

---

# ✅ Checklist final

Antes de considerar pronto:

* [ ] Banco conectado no Railway
* [ ] Django usando PostgreSQL em produção
* [ ] Variáveis configuradas no Vercel
* [ ] Migrations aplicadas
* [ ] Admin criado
* [ ] Sistema funcionando
* [ ] Backup ativo
* [ ] Documentação atualizada

---

# 🧠 Resultado final esperado

Após executar todas as etapas:

* Aplicação rodando em produção
* Banco PostgreSQL estável no Railway
* Deploy funcionando no Vercel
* Sistema pronto para uso real

---

# 🚀 Observação final

Não avance etapas sem validar a anterior.
Esse roteiro transforma seu projeto de **ambiente local → sistema em produção real**.

---
