# Deploy em Producao (HostGator)

## Objetivo

Este guia cobre deploy em HostGator para:

- hospedagem compartilhada com cPanel + Python App (Passenger)
- VPS Linux

As configuracoes abaixo mantem seguranca de producao, suportam MySQL/PostgreSQL por variavel de ambiente e deixam S3 opcional para uploads.

## Diagnostico do projeto e ajustes aplicados

Estado inicial identificado:

- `config.settings.production` exigia PostgreSQL obrigatoriamente
- `config.settings.production` exigia S3 obrigatoriamente
- nao havia entrada `passenger_wsgi.py` para cPanel/Passenger
- documentacao de deploy estava focada em Vercel

Ajustes implementados:

- selecao de banco por variavel (`DATABASE_ENGINE`)
- suporte a MySQL para producao (com `PyMySQL`)
- S3 opcional: sem variaveis AWS completas, usa media local com FileSystemStorage
- novo `passenger_wsgi.py` para HostGator compartilhada
- reforco de seguranca de producao (hosts, CSRF https, cookies seguros, HSTS)
- refatoracao de settings para modulos reutilizaveis:
  - `config/settings/components/env.py`
  - `config/settings/components/database.py`
  - `config/settings/components/storage.py`

## Variaveis de ambiente obrigatorias (producao)

### Aplicacao e seguranca

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DEBUG=0`
- `DJANGO_SECRET_KEY=<segredo-forte>`
- `ALLOWED_HOSTS=SEU-DOMINIO.com,www.SEU-DOMINIO.com`
- `CSRF_TRUSTED_ORIGINS=https://SEU-DOMINIO.com,https://www.SEU-DOMINIO.com`

### Banco de dados (escolha um engine)

- `DATABASE_ENGINE=mysql` (recomendado em HostGator compartilhada)
- ou `DATABASE_ENGINE=postgresql`

Para MySQL:

- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT` (normalmente `3306`)

Para PostgreSQL:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT` (normalmente `5432`)

### Uploads (S3 opcional)

Se todas variaveis AWS estiverem presentes, uploads vao para S3:

- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_CUSTOM_DOMAIN` (opcional)
- `AWS_MEDIA_LOCATION` (opcional, padrao `media`)

Se nao definir AWS (ou remover todas), uploads ficam em `MEDIA_ROOT` local.

## Static e media em producao

- estaticos: `STATIC_ROOT=staticfiles/` + `collectstatic`
- media local: `MEDIA_ROOT=media/`
- para compartilhada, sirva `/static/` e `/media/` via cPanel/Apache (aliases ou regras do host)

## Deploy em HostGator compartilhada (cPanel + Passenger)

## 1) Estrutura no servidor

Suba o projeto para uma pasta fora de `public_html` (exemplo):

- `/home/USUARIO/apps/blog_de_leitura/`

O arquivo `passenger_wsgi.py` deve estar nessa raiz do projeto.

## 2) Criar app Python no cPanel

No cPanel:

1. Entre em `Setup Python App`.
2. Crie app apontando para a pasta do projeto.
3. Defina startup file como `passenger_wsgi.py`.
4. Defina app URL para `https://SEU-DOMINIO.com`.

## 3) Instalar dependencias

Ative o virtualenv gerado pelo cPanel e rode:

```bash
pip install -r requirements.txt
```

## 4) Configurar variaveis de ambiente

No painel da Python App, cadastre as variaveis listadas na secao anterior.

## 5) Migracoes e estaticos

Com o venv ativo:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

## 6) Reiniciar app

No cPanel Python App, clique em `Restart`.

## Deploy em VPS (Ubuntu/Debian exemplo)

Exemplo com Gunicorn + Nginx:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
gunicorn config.wsgi:application --bind 127.0.0.1:8001
```

Configure Nginx como reverse proxy HTTPS para `127.0.0.1:8001`.

## Comandos exatos de publicacao (resumo)

```bash
cd /home/USUARIO/apps/blog_de_leitura
source /home/USUARIO/virtualenv/blog_de_leitura/3.x/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

Depois, reinicie o app no cPanel.

## Troubleshooting

- Erro `Invalid HTTP_HOST header`: revisar `ALLOWED_HOSTS`.
- Erro CSRF em HTTPS: revisar `CSRF_TRUSTED_ORIGINS` com `https://`.
- Erro de conexao MySQL: validar host/usuario/senha e liberacao do usuario no banco.
- Upload nao salva em S3: conferir se todas variaveis AWS foram definidas (parcial gera erro por seguranca).
- Arquivos estaticos nao carregam: executar `collectstatic` e revisar mapeamento `/static/`.
- Erro de permissao em media local: ajustar permissao de escrita da pasta `media/`.

## Registro da refatoracao tecnica

Mudancas de organizacao:

- centralizacao de leitura de env em `components/env.py`
- centralizacao de estrategia de banco em `components/database.py`
- centralizacao de estrategia de storage em `components/storage.py`
- `development.py` e `production.py` agora sao composicoes mais enxutas

Justificativa:

- reduzir duplicacao e acoplamento em settings
- facilitar manutencao e evolucao de ambientes
- permitir HostGator com configuracao segura sem forcar infraestrutura especifica
