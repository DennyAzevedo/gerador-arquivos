# 01 — Stack Tecnológica

Documento que registra a stack sugerida para o projeto e a justificativa de cada escolha.

## Visão geral

| Camada | Tecnologia escolhida |
| ------ | -------------------- |
| Frontend | React + TypeScript + Vite + **Mantine** + TanStack Query + React Router |
| Backend | Python + **FastAPI** + SQLAlchemy 2.0 (async) + Alembic + Pydantic |
| Autenticação | JWT (OAuth2 password flow) via `fastapi-users` |
| IA / Geração | OpenAI SDK (Python) |
| Banco de dados | PostgreSQL (porta `5432` exposta ao host) |
| Infraestrutura | Docker Compose (serviços: `frontend`, `backend`, `db`) |

## Diagrama de arquitetura

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  frontend    │─────►│   backend    │─────►│  postgres    │
│ React+Vite   │ HTTP │   FastAPI    │ SQL  │  :5432 (host)│
│ Mantine :5173│◄─────│   :8000      │◄─────│  volume      │
└──────────────┘      └──────┬───────┘      └──────────────┘
                             │ HTTPS
                             ▼
                        OpenAI API
```

## Backend — Python + FastAPI

- **FastAPI**: framework assíncrono, ideal para chamadas com latência alta (OpenAI), com documentação automática (Swagger/OpenAPI) e validação nativa via Pydantic.
- **SQLAlchemy 2.0 (async)** + **asyncpg**: ORM moderno com suporte assíncrono.
- **Alembic**: versionamento e migração de schema.
- **Pydantic / pydantic-settings**: DTOs e configuração via variáveis de ambiente.
- **fastapi-users**: autenticação completa (registro, login, JWT, hash de senha) integrada ao PostgreSQL.
- **OpenAI SDK**: integração oficial com a LLM geradora de artigos.
- **Uvicorn**: servidor ASGI.

## Frontend — React + TypeScript + Vite

- **Vite**: build e dev server rápidos e modernos (CRA está descontinuado).
- **TypeScript (strict)**: segurança de tipos, essencial para qualidade sem revisão manual.
- **Mantine**: biblioteca de UI escolhida — completa (formulários, notificações, modais, hooks), limpa por padrão e com boa acessibilidade, alinhada aos princípios de UX.
- **TanStack Query**: gerenciamento de server state, cache e estados de carregamento/erro.
- **React Router**: navegação e rotas protegidas.
- **Axios**: cliente HTTP com interceptors para o token JWT.

## Banco de dados — PostgreSQL

- Executado em container com volume persistente (`pgdata`).
- Porta `5432` exposta ao host para inspeção via **DataGrip (JetBrains)** — por isso não há Adminer/pgAdmin no Compose.

## Infraestrutura — Docker Compose

Três serviços:

- `db`: PostgreSQL 16 com `healthcheck` (`pg_isready`).
- `backend`: FastAPI; sobe somente após o banco estar saudável.
- `frontend`: React + Vite; aponta para o backend.

Variáveis sensíveis ficam em `.env` (não versionado), com um `.env.example` versionado como referência.

## Decisões registradas

- **UI**: Mantine (confirmado pelo usuário).
- **Visualização do banco**: nenhuma ferramenta no Compose; uso externo do DataGrip.
- **Modelo OpenAI**: configurável por variável de ambiente (padrão sugerido: `gpt-4o-mini`).
- **Publicação no WordPress**: prevista como etapa futura (roadmap), fora do primeiro ciclo.
