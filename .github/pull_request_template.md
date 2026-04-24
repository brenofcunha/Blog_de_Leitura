# Pull Request

## Descrição

Descreva objetivamente o que foi feito neste PR.

Inclua:

* Qual problema foi resolvido
* Qual funcionalidade foi implementada
* Qual parte do sistema foi afetada

---

## Origem da branch (OBRIGATÓRIO)

Informe o nome completo da branch:

```md
tipo/especificacao-descricao
```

### Tipos aceitos no repositório:

```md
recurso/        → novas funcionalidades
correcao/       → correções de bugs
hotfix/         → correções críticas
copiloto/       → código gerado por IA
```

### Exemplos reais (seguir este padrão):

```md
recurso/livros-crud-de-banco-de-dados
recurso/servico-de-reserva-de-back-end
recurso/formulario-de-reserva-de-front-end
recurso/implantacao-configuracao-docker
recurso/documentacao-readme-atualizacao

correcao/erro-de-conexao-com-o-banco-de-dados

hotfix/falha-de-login

copiloto/recurso-integracao-crud-reserva-servico
```

---

## Regra de escopo da branch (CRÍTICO)

O PR deve respeitar **exatamente o escopo da branch**.

### ✔ Permitido:

* Alterações diretamente relacionadas à descrição da branch

### Proibido:

* Misturar múltiplas áreas (ex: backend + frontend + deploy no mesmo PR)
* Incluir código não relacionado à funcionalidade principal

---

## Diretriz para IA (Copilot, ChatGPT, etc.)

Se este PR for gerado por IA:

* A IA deve interpretar o nome da branch como **fonte de verdade do escopo**
* A IA deve evitar adicionar código fora da responsabilidade da branch
* A IA deve dividir mudanças grandes em múltiplos PRs
* A IA deve priorizar clareza e rastreabilidade

---

## Boas práticas de commits (OBRIGATÓRIO)

Este repositório exige commits pequenos e organizados.

### ✔ Regras:

* Commits devem ser pequenos e frequentes
* Cada commit deve representar uma única responsabilidade
* Commits devem ser legíveis e rastreáveis

### ✔ Formato recomendado:

---

```md
feat(database): create books table
feat(backend): implement reservation service
feat(frontend): add reservation form UI
fix(database): resolve connection error
docs(readme): update installation instructions

---
```

### Evite:

```md
update
ajustes
mudanças gerais
commit final
```

## Organização ideal do PR

Um PR deve conter:

* Até ~10 commits pequenos (preferencial)
* Uma única responsabilidade
* Mudanças fáceis de revisar

Se estiver grande demais → divida em múltiplos PRs.

---

## Como testar

Descreva como validar este PR:

1.
2.
3.

---

## Evidências (se aplicável)

* Logs
* Prints
* Retornos de API
* Testes executados

---

## Impactos no sistema

Marque o que foi afetado:

* [ ] Banco de dados
* [ ] Back-end
* [ ] Front-end
* [ ] Deploy
* [ ] Documentação
* [ ] Segurança
* [ ] Testes
* [ ] Nenhum impacto relevante

Explique se necessário:

```md
```

---

## Regras de integridade do repositório

Para manter um histórico limpo e confiável:

* PRs grandes devem ser evitados
* Cada PR deve ter um propósito claro
* O histórico deve permitir rastrear mudanças facilmente
* Não misturar refatoração com nova funcionalidade no mesmo PR
* Não enviar código quebrado ou incompleto

---

## Checklist obrigatório

Antes de abrir o PR:

* [ ] A branch segue o padrão definido
* [ ] O PR respeita o escopo da branch
* [ ] Os commits são pequenos e organizados
* [ ] O código foi testado localmente
* [ ] Não há código desnecessário
* [ ] A funcionalidade está completa
* [ ] O PR está revisável (não muito grande)

---

## Revisão

Foque em:

* [ ] Escopo da branch
* [ ] Organização dos commits
* [ ] Clareza do código
* [ ] Possíveis bugs
* [ ] Performance
* [ ] Segurança

---

## Issue relacionada

```md
Closes #
```
