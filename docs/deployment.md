# Deploy e Operacao em Producao

## Objetivo

Padronizar o deploy do projeto com seguranca e previsibilidade.

## Ambientes de configuracao

O projeto possui tres modulos de settings:

- config.settings.base
- config.settings.development
- config.settings.production

Em producao, usar obrigatoriamente:

DJANGO_SETTINGS_MODULE=config.settings.production

## Variaveis de ambiente essenciais

### Aplicacao e seguranca

- DJANGO_SECRET_KEY
- DJANGO_ALLOWED_HOSTS (separado por virgula)
- DJANGO_CSRF_TRUSTED_ORIGINS (com https://)
- DJANGO_SECURE_SSL_REDIRECT
- DJANGO_USE_X_FORWARDED_PROTO
- DJANGO_SECURE_HSTS_SECONDS

### Banco PostgreSQL

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT

### Storage de uploads (S3)

- AWS_STORAGE_BUCKET_NAME
- AWS_S3_REGION_NAME
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_S3_CUSTOM_DOMAIN (opcional)

## Estrategia de banco de dados

- desenvolvimento: SQLite por padrao (ou PostgreSQL com USE_POSTGRES=1)
- producao: PostgreSQL obrigatorio

Passos de preparacao:

1. criar banco e usuario no PostgreSQL
2. configurar variaveis de ambiente
3. aplicar migracoes:

python manage.py migrate

## DEBUG e seguranca

Em producao:

- DEBUG deve permanecer desabilitado
- cookies de sessao e CSRF devem ser seguros
- SSL redirect deve permanecer habilitado
- HSTS deve ficar ativo

## Arquivos estaticos e uploads

### Estaticos

- STATIC_ROOT definido como staticfiles/
- executar:

python manage.py collectstatic --noinput

### Uploads

- desenvolvimento: armazenamento local em media/
- producao: armazenamento em S3 via django-storages

## Deploy com Vercel

### Pre-requisitos

- projeto conectado a conta Vercel
- variaveis de ambiente cadastradas no painel
- acesso ao banco PostgreSQL de producao
- bucket S3 configurado para media

### Passos

1. configurar variaveis no painel da Vercel
2. garantir DJANGO_SETTINGS_MODULE=config.settings.production
3. executar deploy
4. validar endpoints publicos e administrativos
5. validar upload de imagem de capa

## Checklist pos-deploy

- aplicacao abre sem erro 500
- login e logout funcionam
- listagem publica exibe apenas posts publicados
- painel admin respeita regras de permissao
- static files carregam corretamente
- upload de imagem funciona em producao

## Troubleshooting rapido

- erro de host invalido: revisar DJANGO_ALLOWED_HOSTS
- erro CSRF em formulario: revisar DJANGO_CSRF_TRUSTED_ORIGINS com https://
- erro de conexao com banco: revisar credenciais/host/porta
- upload quebrado: revisar credenciais AWS e bucket
