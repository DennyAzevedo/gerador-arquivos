# Gerador de Artigos para WordPress

Gerador de artigos com Inteligência Artificial para publicação em blog WordPress. O sistema utiliza a API do **Google Gemini** para gerar conteúdo, oferece uma interface web para configuração e revisão, e persiste os artigos em PostgreSQL.

> **Nota sobre o desenvolvimento:** Este projeto é desenvolvido integralmente com o [Cursor](https://cursor.com) como ferramenta de codificação assistida por IA, **sem intervenção manual no código**. O objetivo é validar e demonstrar um fluxo de desenvolvimento orientado por agentes de IA.

## Documentação

A documentação completa está na pasta [`docs/`](docs/README.md):

| Documento | Conteúdo |
| --------- | -------- |
| [01 — Stack](docs/01-stack.md) | Tecnologias e justificativas |
| [02 — Planejamento](docs/02-planejamento.md) | Arquitetura, pastas, API |
| [03 — Regras](docs/03-regras-codificacao.md) | Padrões de codificação |
| [04 — Etapas](docs/04-etapas-execucao.md) | Roteiro de fases (concluído) |

## Funcionalidades

- Autenticação JWT (registro, login, sessão)
- Geração de artigos via Gemini (tema, palavras-chave, tom)
- Publicação no WordPress (mock por padrão; integração real configurável)
- Preview editável antes de salvar
- CRUD de artigos (rascunho / publicado)
- Interface responsiva (React + Mantine)

## Arquitetura

```
   Docker Compose                              Host
┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
│  frontend    │─────►│   backend    │─────►│  PostgreSQL      │
│ React+Vite   │ HTTP │   FastAPI    │ SQL  │  (container host)│
│ Mantine :5173│◄─────│   :8000      │◄─────│  localhost:5432  │
└──────────────┘      └──────┬───────┘      └──────────────────┘
                             │ HTTPS
                             ▼
                        Gemini API
```

O PostgreSQL **não** faz parte do `docker-compose.yml`: o backend conecta a uma instância existente no host via `host.docker.internal:5432`.

## Stack

| Camada | Tecnologia |
| ------ | ---------- |
| Frontend | React 19, TypeScript, Vite, Mantine 9, TanStack Query, React Router |
| Backend | Python 3.12, FastAPI, SQLAlchemy 2 (async), Alembic, Pydantic, fastapi-users |
| IA | Google Gemini API (`google-genai`, `gemini-2.0-flash` por padrão) |
| Banco | PostgreSQL |
| Infra | Docker Compose (frontend + backend) |

## Estrutura do projeto

```
gerador-arquivos/
├── backend/
│   ├── src/app/           # api, application, domain, infrastructure
│   ├── migrations/        # Alembic
│   ├── tests/             # pytest (unit, integration, api)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/               # features (auth, articles), shared, app
│   ├── tests/             # Vitest
│   ├── package.json
│   └── Dockerfile
├── docs/                  # documentação do projeto
├── docker-compose.yml
├── .env.example           # template de variáveis (versionado)
└── README.md
```

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e Docker Compose
- PostgreSQL acessível (container ou instalação local na porta `5432`)
- Chave de API do [Google Gemini](https://aistudio.google.com/apikey)

## Configuração e execução

### 1. Variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais reais. **Nunca commite o arquivo `.env`** — ele já está no `.gitignore`.

| Variável | Descrição |
| -------- | --------- |
| `DATABASE_URL` | Conexão async do backend ao PostgreSQL |
| `GEMINI_API_KEY` | Chave da API Gemini ([Google AI Studio](https://aistudio.google.com/apikey)) |
| `GEMINI_MODEL` | Modelo Gemini (padrão: `gemini-2.0-flash`) |
| `WORDPRESS_MOCK` | `true` = envio simulado (padrão); `false` = publicação real |
| `WORDPRESS_URL` | URL base do blog (ex.: `https://meublog.com`) |
| `WORDPRESS_USERNAME` | Usuário WordPress (obrigatório se mock=false) |
| `WORDPRESS_APP_PASSWORD` | Senha de aplicativo WordPress (obrigatório se mock=false) |
| `JWT_SECRET` | Segredo para tokens JWT (mín. 32 caracteres em produção) |
| `CORS_ORIGINS` | Origens permitidas (ex.: `http://localhost:5173`) |
| `VITE_API_URL` | URL do backend acessada pelo navegador |

**Senhas com caracteres especiais:** codifique na `DATABASE_URL` (ex.: `@` → `%40`).

### 2. Banco de dados

Crie o banco do projeto no PostgreSQL (se ainda não existir):

```bash
psql -U seu_usuario -c "CREATE DATABASE gerador_artigos;"
```

**DataGrip:** conecte em `localhost:5432` com o usuário do `.env`, mas selecione o banco **`gerador_artigos`** (não `denny` nem `postgres` — esses bancos existem por padrão, porém ficam vazios). As tabelas ficam em `schemas → public → tables` (`users`, `articles`, `alembic_version`).

### 3. Migrações

```bash
docker compose run --rm backend alembic upgrade head
```

### 4. Subir a aplicação

```bash
docker compose up --build
```

| Serviço | URL |
| ------- | --- |
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger (docs) | http://localhost:8000/docs |

### 5. Fluxo de uso

1. Acesse http://localhost:5173 e crie uma conta
2. Faça login
3. Em **Gerar artigo**, informe tema/palavras-chave e clique em **Gerar**
4. Revise o conteúdo gerado e **Salvar**
5. Gerencie artigos no **Dashboard** (editar, excluir, alterar status)
6. Clique em **Publicar no WordPress** para enviar (simulado enquanto `WORDPRESS_MOCK=true`)

## Testes

Requer banco de testes `gerador_artigos_test` (separado do banco de desenvolvimento):

```bash
psql -U seu_usuario -c "CREATE DATABASE gerador_artigos_test;"
```

**Backend** (pytest — 22 testes):

```bash
docker compose run --rm \
  -e DATABASE_URL="postgresql+asyncpg://USER:SENHA@host.docker.internal:5432/gerador_artigos_test" \
  backend sh -c "pip install -r requirements-dev.txt && pytest"
```

**Frontend** (Vitest — 13 testes):

```bash
docker compose run --rm --no-deps frontend sh -c "npm install && npm run test"
```

## Segurança

- Credenciais ficam **somente** no `.env` local (nunca versionado)
- Use `.env.example` como referência com placeholders
- Em produção, injete segredos via gerenciador de configuração (Vault, secrets do CI/CD, etc.)
- Rotacione `JWT_SECRET`, senha do banco e `GEMINI_API_KEY` se houver exposição acidental

## Roadmap

### Concluído

- [x] Backend FastAPI (camadas DDD, CQRS, Gemini, CRUD)
- [x] Frontend React + Mantine (auth, dashboard, geração, edição)
- [x] Docker Compose (frontend + backend)
- [x] Testes automatizados (pytest + Vitest)
- [x] Documentação em `docs/`
- [x] Migração OpenAI → Gemini

### Próximos passos

- [x] Integração WordPress mockada (porta + adapter + endpoint + UI)
- [ ] Agendamento de publicações
- [ ] CI/CD (GitHub Actions: lint, testes, build)
- [ ] Preview Markdown renderizado no frontend
- [ ] Suporte a múltiplos sites WordPress por usuário

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
