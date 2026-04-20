# PostgreSQL no Railway (Etapa 2)

## Objetivo

Provisionar um banco PostgreSQL no Railway para producao, identificar variaveis de conexao e validar acesso externo.

## Escopo da Etapa 2

Esta etapa cobre:

- criacao do servico PostgreSQL no Railway
- identificacao das variaveis de conexao
- documentacao da conexao para uso no deploy
- validacao de acessibilidade externa

Esta etapa ainda nao altera o codigo da conexao do Django (isso entra na Etapa 3).

## 1. Criar servico PostgreSQL no Railway

1. Acesse seu projeto no Railway.
2. Clique em New Service.
3. Selecione PostgreSQL.
4. Aguarde o provisionamento concluir.

Resultado esperado:

- servico de banco criado
- credenciais disponiveis na aba Variables ou Connect

## 2. Identificar variaveis de conexao

No Railway, capture os dados abaixo.

### Opcao A (recomendada): URL unica

- DATABASE_URL

Formato esperado:

postgresql://USER:PASSWORD@HOST:PORT/DBNAME

### Opcao B: variaveis separadas

- PGHOST
- PGPORT
- PGDATABASE
- PGUSER
- PGPASSWORD

No projeto atual (antes da Etapa 3), o settings de producao usa variaveis no formato:

- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

Mapeamento sugerido:

- PGHOST -> POSTGRES_HOST
- PGPORT -> POSTGRES_PORT
- PGDATABASE -> POSTGRES_DB
- PGUSER -> POSTGRES_USER
- PGPASSWORD -> POSTGRES_PASSWORD

## 3. Validar acesso externo ao banco

Escolha uma das validacoes abaixo.

### Validacao com psql

Comando exemplo:

psql "postgresql://USER:PASSWORD@HOST:PORT/DBNAME" -c "select now();"

Resultado esperado:

- comando executa sem timeout
- retorna timestamp do servidor

### Validacao com Python (psycopg2)

Comando exemplo:

python -c "import psycopg2; conn=psycopg2.connect('postgresql://USER:PASSWORD@HOST:PORT/DBNAME'); cur=conn.cursor(); cur.execute('select 1'); print(cur.fetchone()); conn.close()"

Resultado esperado:

- imprime (1,)

### Validacao de rede (Windows)

PowerShell:

Test-NetConnection HOST -Port PORT

Resultado esperado:

- TcpTestSucceeded = True

## 4. Regras de seguranca

- nao versionar credenciais reais no repositio
- nunca expor DATABASE_URL em prints de log
- registrar apenas placeholders na documentacao

## 5. Registro operacional (preencher)

Preencha apos criar no Railway:

- ambiente: producao
- provedor: Railway PostgreSQL
- host publico: [preencher]
- porta: [preencher]
- database: [preencher]
- validacao externa executada: [sim/nao]
- data da validacao: [preencher]

## 6. Criterio de pronto da Etapa 2

- servico PostgreSQL criado no Railway
- variaveis de conexao identificadas
- conexao externa validada com sucesso
- dados registrados em documentacao interna
